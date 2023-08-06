# -*- coding: uTf-8 -*-
import glob
import os
from chardet.universaldetector import UniversalDetector
import csv


class FileSearcher():
    search_path_results = []
    search_index_results = []
    search_word_results = []

    # 相対パス -> 絶対パス
    def listup_files(self, path):
        yield [os.path.abspath(p) for p in glob.glob(path)]

    # ファイルの文字コードを取得
    def get_file_encoding(self, file_path):
        detector = UniversalDetector()
        with open(file_path, mode='rb') as f:
            for binary in f:
                detector.feed(binary)
                if detector.done:
                    break
        detector.close()
        return detector.result['encoding']

    def get_paths(self, dir_path):
        file_abs_paths = []

        for dir_path, subdir_paths, subfile_paths in os.walk(dir_path):
            for filepath in subfile_paths:
                file_abs_paths.append(dir_path + '\\' + filepath)

        return {"file_abs_path": file_abs_paths,
                "subdir_path": subdir_paths,
                "subfile_path": subfile_paths
        }

    # キーワード検索
    def search_words(self, file_path, keywords, ignore_exts=None):
        print("------------------------")
        print("Load：" + file_path)
        encoding = self.get_file_encoding(file_path)

        # ファイルの中身を1行ずつ読み込んでリストに格納
        with open(file_path, mode='r', newline='', encoding=encoding) as f_in:
            lines = [line for line in f_in]

        # リストから1行文ずつデータを取り出し、検索ワードが含まれているかチェック
        for line in lines:
            for keyword in keywords:
                if keyword in line:
                    self.search_index_results.append(str(lines.index(line)))
                    self.search_word_results.append(keyword)
                    self.search_path_results.append(file_path)
                    print("index:" + str(lines.index(line) + 1) + ", word:" + keyword)

    # キーワード検索
    def search_words_infiles(self, file_paths, keywords, ignore_exts=None):
        for file_path in file_paths:
            # 検索対象からの除外フラグを初期化
            ignore_flag = False

            # 除外対象の拡張子が含まれているか確認
            for ignore_ext in ignore_exts:
                # 除外対象の拡張子があれば、除外フラグを立てる
                if ignore_ext in file_path:
                    ignore_flag = True
                    break

            # 検索対象がディレクトリでなく、かつ除外対象フラグも立っていなければ探索
            if os.path.isdir(file_path) == False and ignore_flag == False:
                try:
                    self.search_words(file_path, keywords=keywords)
                except:
                    print("Load Error:" + file_path)
                    import traceback
                    traceback.print_exc()

        return [self.search_index_results,
                self.search_word_results,
                self.search_path_results
        ]

    # 結果の保存
    def save_result(self, save_file_path, result):    
        with open(save_file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(list(zip(*result)))

def main():
    fsearch = FileSearcher()

    # 検索ワード
    KEYWORDS= ["test", "tes"]
    
    # 無視するファイル形式の拡張子
    IGNORE_EXTS = [".jpg", ".png", ".pdf", ".vs", ".py"]

    # 検索対象のパス
    LOAD_DIR_PATH = "C:/github/sample/python/file"

    # 検索結果の出力先
    SAVE_FILE_PATH = "C:/github/sample/python/result.csv"

    # 検索対象内の全てのファイル・フォルダパスを取得
    paths = fsearch.get_paths(LOAD_DIR_PATH)

    # すべてのフォルダにあるファイルを対象に、中身に検索キーワードが含まれているかチェック
    result = fsearch.search_words_infiles(paths["file_abs_path"], keywords=KEYWORDS,
                                 ignore_exts=IGNORE_EXTS)
    
    fsearch.save_result(SAVE_FILE_PATH, result)

"""
3,test,C:/github/sample/python/file\sample.txt
3,tes,C:/github/sample/python/file\sample.txt
3,test,C:/github/sample/python/file\search_words.py
3,tes,C:/github/sample/python/file\search_words.py
23,test,C:/github/sample/python/file\search_words.py
23,tes,C:/github/sample/python/file\search_words.py
61,test,C:/github/sample/python/file\search_words2.py
61,tes,C:/github/sample/python/file\search_words2.py
"""

if __name__ == "__main__":
    main()
