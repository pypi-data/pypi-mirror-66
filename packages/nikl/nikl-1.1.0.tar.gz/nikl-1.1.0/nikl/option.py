"""
Implement parameter options
"""
import argparse
from argparse import RawTextHelpFormatter


def setting_parse():
    """
        Setting input format

        Returns:
            :param: filename(array): the name array of files
            :param: newline(boolean): add '\n' in pre-processed result(.txt)
            :param: info(boolean): select to get the information of .txt file, <teiHeader></teiHeader>
            :param: content(boolean): select to get the content of .txt file, <text></text>
    """
    parser = argparse.ArgumentParser(description='옵션을 선택해주세요.', formatter_class=RawTextHelpFormatter)
    parser.add_argument('--filenames', required=True, nargs='+', help='전처리 할 txt 파일명을 입력해주세요: text1.txt text2.txt text3.txt\n'
                                                                      '한 개 이상의 값을 입력해주세요.\n\n')
    parser.add_argument('--info', required=False, action='store_true', help='해당 txt 파일의 정보를 추출할건지 알려주세요: [True / False]\n'
                                                                            '기본값은 False 입니다.\n\n')
    parser.add_argument('--content', required=False, action='store_true', help='해당 txt 파일의 내용을 추출할건지 알려주세요: [True / False]\n'
                                                                               '기본값은 True 입니다.\n\n')
    parser.add_argument('--newline', required=False, action='store_true',
                        help='전처리 결과값에 단락 별 개행문자 적용 여부를 알려주세요: [True / False]\n'
                             '기본값은 True 입니다.\n\n')

    args = parser.parse_args()
    filenames, info, content, newline = args.filenames, args.info, args.content, args.newline
    return filenames, info, content, newline
