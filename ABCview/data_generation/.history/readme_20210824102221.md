# generate attribution score/ attention score
python examples/generate_attrscore.py --task_name mnli --data_dir /home/newdisk/szk/tf_vis/attattr/ --bert_model bert-base-cased --batch_size 16 --num_batch 4  --model_file model.mnli.bin --get_att_attr --get_att_score --output_dir output
# get tokens and predictions and hidden states
python examples/get_tokens_and_pred_and_hidden_states.py --data_dir /home/newdisk/szk/tf_vis/attattr/  --bert_model bert-base-cased  --task_name mnli --model_file model.mnli.bin --output_dir output
# generate attribution tree
python examples/attribution_tree.py --attr_file output/attr_zero_base_exp5.json --tokens_file output/tokens_and_pred_100.json --task_name mnli --example_index 5
# generate head importance
python examples/prune_head_with_attr.py --task_name mnli --data_dir /home/newdisk/szk/tf_vis/attattr/ --bert_model bert-base-cased --model_file model.mnli.bin  --output_dir output

# 使用mnli语料库进行预训练得到的模型参数存在model.mnli.bin中，运行上述代码获得的数据文件存于output中，实际使用为了统一还需要修改一些命令，如example_index等

待优化：
生成隐层状态的词向量：把max_len缩减到输入tokens的len以加快运算，不然每次都用128会增大很多开销和耗时
利用encoded_layers生成tsne相关数据的.py文件应与get hidden states代码合并优化，后续还要调整
如果要实时前后端传输的话需要把模型等相关的提前download到服务器，用URL去网上下载耗时很多
由于部分代码是从attattr开源代码库中节选并修改，因此代码内部可能还存在一些冗余，之后需要处理掉

待解决：
暂时没有解决生成saliency score的代码，可能是因为transformer库版本变化的原因，一直报错
后续可以尝试用https://github.com/cdpierse/transformers-interpret 里的方法试试

# 数据集和模型参数>100M，暂时先不上传
