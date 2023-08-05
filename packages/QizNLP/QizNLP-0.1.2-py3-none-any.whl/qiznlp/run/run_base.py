import os, pickle, glob
import tensorflow as tf
import numpy as np

import qiznlp.common.utils as utils
import qiznlp.common.train_helper as train_helper


class Run_Model_Base():
    def __init__(self):
        self.model_name = None
        self.sess = None
        self.graph = None
        self.config = None
        self.saver = None
        self.token2id_dct = None
        self.tokenize = None
        self.cut = None
        self.use_hvd = None
        self.model = None

    def save(self, ckpt_dir, model_name=None, epo=None, global_step=None, info_str=''):
        if hasattr(self, 'hvd_rank') and self.hvd_rank != 0:  # 分布式训练时只需1个进程master来保存
            return
        if not os.path.exists(ckpt_dir): os.makedirs(ckpt_dir)
        if model_name is None: model_name = self.model_name
        if global_step is None: global_step = self.model.global_step
        epo = '' if epo is None else f'{epo}-'

        save_path = f'{ckpt_dir}/{model_name}-{epo}{info_str}.ckpt'

        exist_ckpt_path = glob.glob(f'{ckpt_dir}/{model_name}-{epo}*')
        if exist_ckpt_path:
            ckpt_path = exist_ckpt_path[0].rsplit('.', 1)[0]
            [utils.delete_file(file) for file in [
                ckpt_path + '.index',
                ckpt_path + '.meta',
                ckpt_path + '.data-00000-of-00001'
            ]]

        self.saver.save(self.sess, save_path, global_step=global_step)
        # e.g.
        # mrfn-2-1.23-1.18.ckpt-228.index
        # mrfn-2-1.23-1.18.ckpt-228.meta
        print(f'>>>>>> save ckpt ok! {save_path}')

    def restore(self, ckpt_dir, model_name=None, epo=None, step=None):
        if model_name is None: model_name = self.model_name
        if epo is not None:
            restore_path = glob.glob(f'{ckpt_dir}/{model_name}-{epo}-*.ckpt*')[0].rsplit('.', 1)[0]
        elif step is not None:
            restore_path = glob.glob(f'{ckpt_dir}/{model_name}*.ckpt-{step}.*')[0].rsplit('.', 1)[0]
        else:
            restore_path = tf.train.latest_checkpoint(ckpt_dir)
        self.saver.restore(self.sess, restore_path)
        print(f'<<<<<< restoring ckpt from {restore_path}')

    def delete_ckpt(self, ckpt_dir, model_name=None, epo=None):
        if model_name is None: model_name = self.model_name
        if epo is None:  # 删除所有的epo
            epo = ''
        exist_ckpt_path = glob.glob(f'{ckpt_dir}/{model_name}-{epo}*')
        if exist_ckpt_path:  # 如果存在就删除
            ckpt_path = exist_ckpt_path[0].rsplit('.', 1)[0]
            res = [utils.delete_file(file, verbose=False) for file in [
                ckpt_path + '.index',
                ckpt_path + '.meta',
                ckpt_path + '.data-00000-of-00001']]
            if all(res):
                print(f'delete {ckpt_path} success!')

    def prepare_data(self, data_type, raw_data_file,
                     preprocess_raw_data, batch_size,
                     save_data_prefix,
                     **kwargs):
        index = self.hvd_rank if hasattr(self, 'hvd_rank') else None
        shard = self.hvd_size if hasattr(self, 'hvd_size') else None

        if data_type == 'tfrecord':
            train_tfrecord_file, dev_tfrecord_file, test_tfrecord_file = train_helper.prepare_tfrecord(
                raw_data_file, self.model, self.token2id_dct, self.tokenize,
                preprocess_raw_data_fn=preprocess_raw_data,
                save_data_prefix=save_data_prefix,
                **kwargs,
            )

            # 如果载入不成功将返回None, None
            train_dataset, train_data_size = self.model.load_tfrecord(train_tfrecord_file, batch_size=batch_size, index=index, shard=shard)
            dev_dataset, dev_data_size = self.model.load_tfrecord(dev_tfrecord_file, batch_size=batch_size)
            test_dataset, test_data_size = self.model.load_tfrecord(test_tfrecord_file, batch_size=batch_size)

            with self.graph.as_default():
                train_features = train_dataset.make_one_shot_iterator().get_next() if train_dataset else None
                dev_features = dev_dataset.make_one_shot_iterator().get_next() if dev_dataset else None
                test_features = test_dataset.make_one_shot_iterator().get_next() if test_dataset else None

            def gen_feed_dict(i, epo, mode='train'):
                nonlocal train_features, dev_features
                if mode == 'train':
                    assert train_features
                    features = self.sess.run(train_features)
                    if i == 0 and epo == 1:
                        print('inspect tfrecord features:')
                        for k, v in features.items():
                            print(f'{k}: {v.shape}{v.tolist()[:2]}')
                    return self.model.create_feed_dict_from_features(features, 'train')
                elif mode == 'dev':
                    assert dev_features
                    features = self.sess.run(dev_features)
                    return self.model.create_feed_dict_from_features(features, 'dev')
                elif mode == 'test':
                    assert test_features
                    features = self.sess.run(test_features)
                    return self.model.create_feed_dict_from_features(features, 'test')
                else:
                    raise Exception('unsupport mode type')


        elif data_type == 'pkldata':
            train_pkl_file, dev_pkl_file, test_pkl_file = train_helper.prepare_pkldata(
                raw_data_file, self.model, self.token2id_dct, self.tokenize,
                preprocess_raw_data_fn=preprocess_raw_data,
                save_data_prefix=save_data_prefix,
                **kwargs,
            )
            train_data, dev_data, test_data, train_data_size, dev_data_size, test_data_size = (None,) * 6
            trn_total_ids, dev_total_ids, test_total_ids = (None,) * 3
            if os.path.exists(train_pkl_file):
                train_data = pickle.load(open(train_pkl_file, 'rb'))
                train_data_size = train_data['num_data']
                print(f'loading exist train pkl file ok! {train_pkl_file}')
            if os.path.exists(dev_pkl_file):
                dev_data = pickle.load(open(dev_pkl_file, 'rb'))
                dev_data_size = dev_data['num_data']
                print(f'loading exist dev pkl file ok! {dev_pkl_file}')
                dev_total_ids = list(range(dev_data_size))  # dev 按顺序就行
            if os.path.exists(test_pkl_file):
                test_data = pickle.load(open(test_pkl_file, 'rb'))
                test_data_size = test_data['num_data']
                print(f'loading exist test pkl file ok! {test_pkl_file}')
                test_total_ids = list(range(test_data_size))  # test 按顺序就行

            curr_epo = -1

            def gen_feed_dict(i, epo, mode='train'):
                nonlocal curr_epo, trn_total_ids, dev_total_ids, test_total_ids, train_data, dev_data, test_data
                if mode == 'train':
                    assert train_data
                    if curr_epo != epo:  # 换了一个epo了
                        np.random.seed(epo)
                        trn_total_ids = np.random.permutation(train_data_size)  # 根据不同epo从新打乱数据
                        curr_epo = epo
                    if i == 0 and epo == 1:
                        print('inspect pkl data:')
                        for k in train_data:
                            if k != 'num_data':
                                v = [train_data[k][i] for i in trn_total_ids[:2]]
                                print(f'{k}: {v}')
                    ids = trn_total_ids[i * batch_size:(i + 1) * batch_size]
                    return self.model.create_feed_dict_from_data(train_data, ids, 'train')
                elif mode == 'dev':
                    assert dev_data
                    dev_ids = dev_total_ids[i * batch_size:(i + 1) * batch_size]
                    return self.model.create_feed_dict_from_data(dev_data, dev_ids, 'dev')
                elif mode == 'test':
                    assert test_data
                    test_ids = test_total_ids[i * batch_size:(i + 1) * batch_size]
                    return self.model.create_feed_dict_from_data(test_data, test_ids, 'test')
                else:
                    raise Exception('unsupport mode type')
        else:
            raise Exception('unsupport data type')

        train_epo_steps, dev_epo_steps, test_epo_steps = (None,) * 3
        if train_data_size:
            train_epo_steps = int(np.ceil(train_data_size / batch_size))
        if dev_data_size:
            dev_epo_steps = int(np.ceil(dev_data_size / batch_size))
        if test_data_size:
            test_epo_steps = int(np.ceil(test_data_size / batch_size))
        print('batch_size:', batch_size)
        print('train_data_size:', train_data_size)
        print('train_epo_steps:', train_epo_steps)
        print('dev_data_size:', dev_data_size)
        print('dev_epo_steps:', dev_epo_steps)
        print('test_data_size:', test_data_size)
        print('test_epo_steps:', test_epo_steps)

        return train_epo_steps, dev_epo_steps, test_epo_steps, gen_feed_dict

    def stop_training(self, early_stop_patience, train_info, indicator='dev_acc', greater_is_better=True):
        # e.g. patience=3 第2、3、4epo都低于第1epo, 则停止
        if not train_info:
            return False
        assert indicator in list(train_info.values())[0], f'indicator {indicator} not in train_info'
        patience = early_stop_patience
        epo_list = sorted(train_info.keys())
        if len(epo_list) <= patience:
            return False
        pivot = epo_list[-(patience + 1)]
        flags = []
        for e in epo_list[-patience:]:
            if greater_is_better:  # 指标越大越好,如准确率
                flags.append(train_info[pivot][indicator] >= train_info[e][indicator])  # 第1轮比第2、3、4指标都好则停止
            else:  # 指标越小越好,如loss
                flags.append(train_info[pivot][indicator] <= train_info[e][indicator])  # 第1轮比第2、3、4指标都好则停止
        return all(flags)

    def should_save(self, curr_epo, train_info, indicator='dev_acc', greater_is_better=True):
        if not train_info:
            return True
        if len(train_info) == 1:
            return True
        assert indicator in list(train_info.values())[0], f'indicator {indicator} not in train_info'
        indicator_lst = [train_info[e][indicator] for e in train_info if e != curr_epo]
        best_indicator = max(indicator_lst) if greater_is_better else min(indicator_lst)
        if greater_is_better:
            if train_info[curr_epo][indicator] > best_indicator:
                return True
            else:
                return False
        else:
            if train_info[curr_epo][indicator] < best_indicator:
                return True
            else:
                return False

    def get_best_epo(self, train_info, indicator='dev_acc', greater_is_better=True):
        if not train_info:
            return 0
        if len(train_info) == 1:
            return 1
        assert indicator in list(train_info.values())[0], f'indicator {indicator} not in train_info'
        indicator_lst = [[epo, v[indicator]] for epo, v in train_info.items()]
        indicator_lst.sort(key=lambda e: e[0], reverse=True)  # 优先后面的epo
        indicator_lst.sort(key=lambda e: e[1], reverse=True if greater_is_better else False)
        return indicator_lst[0][0]

    def export_model(self, pbmodel_dir):
        with self.graph.as_default():  # 坑
            builder = tf.saved_model.builder.SavedModelBuilder(pbmodel_dir)

            inputs, outputs = self.model.get_signature_export_model()
            signature_def_inputs = {k: tf.saved_model.utils.build_tensor_info(v) for k, v in inputs.items()}
            signature_def_outputs = {k: tf.saved_model.utils.build_tensor_info(v) for k, v in outputs.items()}

            default_key = tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY  # or 'chitchat_predict' 签名
            signature_def_map = {default_key:
                tf.saved_model.signature_def_utils.build_signature_def(
                    inputs=signature_def_inputs,
                    outputs=signature_def_outputs,
                    method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME
                )
            }
            builder.add_meta_graph_and_variables(
                self.sess,
                [tf.saved_model.tag_constants.SERVING],
                signature_def_map=signature_def_map
            )
            builder.save(as_text=False)
            print(f'export pb model ok! {pbmodel_dir}')
            return pbmodel_dir
