import setuptools
setuptools.setup(
    name = "mc_wordcloud",
    version = "0.0.9",
    author = "魔扣少儿编程",
    author_email = "2443927272@qq.com",
    url = "https://github.com/LucasKKK/mc_wordcloud", 
    data_files = [('mc_wordcloud', [
        'mc_wordcloud/1.jpg',
        'mc_wordcloud/1.txt',
        'mc_wordcloud/2.jpg',
        'mc_wordcloud/2.txt',
        'mc_wordcloud/3.jpg',
        'mc_wordcloud/3.txt',
        'mc_wordcloud/4.jpg',
        'mc_wordcloud/4.txt',
        'mc_wordcloud/5.jpg',
        'mc_wordcloud/5.txt',
        'mc_wordcloud/6.jpg',
        'mc_wordcloud/6.txt',
        'mc_wordcloud/7.jpg',
        'mc_wordcloud/7.txt',
        'mc_wordcloud/8.jpg',
        'mc_wordcloud/8.txt',
        'mc_wordcloud/9.jpg',
        'mc_wordcloud/9.txt',
        'mc_wordcloud/10.jpg',
        'mc_wordcloud/10.txt',
        'mc_wordcloud/11.jpg',
        'mc_wordcloud/11.txt'
    ])
    ],
    packages = ['mc_wordcloud'],     #多个文件夹手动添加
    include_package_data = True,
    #packages = setuptools.find_packages(),
    install_requires = ['wordcloud', 'numpy', 'matplotlib', 'pillow']
)
