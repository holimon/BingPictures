import argparse

from crawler import CrawPictures

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="data/samples", help="path to dataset")
    parser.add_argument("--keyword", type=str, help="search key")
    parser.add_argument("--prefix", type=str, default='image', help="image's prefix")
    parser.add_argument("--suffix", type=str, default='jpg', help="image's suffix")
    parser.add_argument("--offset", type=int, default=0, help="image's index offset")
    parser.add_argument("--maxnum", type=int, default=100, help="number of images")
    parser.add_argument("--genlist", type=bool, default=False, help="generate image's list")

    opt = parser.parse_args()
    print(opt)

    ins = CrawPictures(opt.folder,opt.keyword,opt.prefix,opt.suffix,opt.offset,opt.maxnum,'bing',opt.genlist)
    ins.run()
    ins.quit()