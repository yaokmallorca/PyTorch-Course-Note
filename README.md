# PyTorch-Course-Note

数据集过大,上传到了百度云 链接: https://pan.baidu.com/s/1YGJ-SR1XMp-TLB-mZryqzA  密码: t2i0 解压后放到目录下即可

#### win10运行问题解决办法:
找到 tornado/platform/asyncio.py 文件修改，添加代码如下：

```python
if sys.platform == 'win32':
 asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


```



###  visdom安装

- git clone git@github.com:facebookresearch/visdom.git
- cd visdom/
- pip install -e .