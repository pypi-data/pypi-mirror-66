# Pynori

Lucene Nori, Korean Mopological Analyzer, in Python

* Nori in Apache Lucene is a korean morpological analyzer based on Mecab.
* Pynori is a python-version of nori (Apache Lucene is written in Java).
* The analysis results are the same (All test cases are passed).
* Pynori maybe a little slower than nori in Elasticsearch because of python script language and less optimized data structures.
* Pynori includes mecab-ko-dic-2.1.1-20180720 for system dictionary.
* Pynori is compatible with Python 3.7 and is distributed under the Apache License 2.0.

자바로 작성되어 있는 아파치 루씬의 노리 형태소 분석기를 파이썬으로 변환한 프로젝트입니다. 원본과 같은 테스트를 실시하여 동일한 결과를 얻었습니다(ref.Test). 정확도는 동일하지만 스크립트 언어인 점과 단순한 Trie 자료구조 사용 등으로 속도는 조금 느립니다(ref.Property & Comparision Study). 동의어 확장 필터를 포함한 진행하지 못한 일들은 앞으로 보완할 계획입니다(ref.TODO).

노리 형태소 분석기에 대한 내용은 저의 [노리 Deep Dive 블로그](https://gritmind.github.io/2019/05/nori-deep-dive.html)를 참고해주세요.

## Install

```
pip install pynori
```


## Usage

```python
from pynori.korean_analyzer import KoreanAnalyzer
nori = KoreanAnalyzer(decompound_mode='MIXED',
                      discard_punctuation=True,
                      output_unknown_unigrams=False,
                      pos_filter=False,
                      stop_tags=['JKS', 'JKB', 'VV', 'EF'])

input_text = "아빠가 방에 들어가신다."
result = nori.do_analysis(input_text)
print(result)
```
```
>>>
{'termAtt': ['아빠', '가', '방', '에', '들어가', '시', 'ᆫ다'],
 'offsetAtt': [(0, 2), (2, 3), (4, 5), (5, 6), (7, 10), (10, 12), (10, 12)],
 'posLengthAtt': [1, 1, 1, 1, 1, 1, 1],
 'posTypeAtt': ['MORP', 'MORP', 'MORP', 'MORP', 'MORP', 'MORP', 'MORP'],
 'posTagAtt': ['NNG', 'JKS', 'NNG', 'JKB', 'VV', 'EP', 'EF'],
 'dictTypeAtt': ['KN', 'KN', 'KN', 'KN', 'KN', 'KN', 'KN']}
```

* KoreanAnalyzer argument.
   * decompound_mode - 복합명사 처리 방식 결정
      * 'MIXED': 원형과 서브단어 모두 출력
      * 'DISCARD': 서브단어만 출력
      * 'NONE': 원형만 출력
   * discard_punctuation - 구두점 제거 여부
   * output_unknown_unigrams - 언논 단어를 음절 단위로 쪼갬 여부
   * pos_filter - POS 필터 실행 여부
   * stop_tags - 필터링되는 POS 태그 리스트 (pos_filter=True일 때만 활성)

## Resources

* 시스템 사전은 `~/pynori/resources/mecab-ko-dic-2.1.1-20180720` 에서 수정
   * 기존 csv 파일 수정/삭제 or 새로운 csv 파일 추가 (mecab 규칙에 맞게 단어 추가 & csv 파일로 추가)
   * csv 파일 변경사항이 있으면, `~/pynori/resources/pkl_mecab_csv/mecab_csv.pkl` 를 삭제해야 함. (초기화시 최신 csv 파일을 기반으로 재생성됨)
* 사용자 사전은 `~/pynori/resources/userdict_ko.txt` 에서 수정 (수정만 하면 곧바로 적용 o)
* 동의어 사전은 `~/pynori/resources/synonyms.txt.txt` 에서 수정 (수정만 하면 곧바로 적용 o)

## Test

```
git clone https://github.com/gritmind/python-nori.git
cd python-nori
python -m unittest -v tests.test_korean_analyzer
python -m unittest -v tests.test_korean_tokenizer
```

## Property

* 최대한 원본 코드와 비슷하게 구현 (변수/파일 이름, 코드 패턴 등)
* Based on Lucene analyzer, nori
* Use mecab-ko-dic-2.1.1-20180720
* Use Trie data structure, instead of FST
* Modify token & dictionary objects
* Not use circular buffer & wordID
* 원본 루씬 노리 대비 개선점
   * 토큰 정보 (Unknown/Known/User, POS type) 출력
   * 특수문자로 시작되는 사용자 단어가 있을 시 동의어 처리가 되지 않는 오류 해결
   
## TODO

* Character Filter
* Synonym Graph Filter
* KoreanTokenizer TODO List (MAX_BACKTRACE_GAP, isLowSurrogate, UnicodeScript ...)
* 속도 향상을 위한 알고리즘 및 자료구조 최적화
* 원본 루씬 노리 대비 개선점
   * Unknown 길이가 무분별하게 길어지는 현상


## Comparision Study

|                 | 한나눔 0.8.4      | 꼬꼬마 2.0     | 트위터 1.14.7   | Pynori 0.1.0    |
| :-------------: | :-------------: |:-------------:|:-------------:|:-------------:|
| 1 개             | 0.00138 sec     | 0.00244 sec   | 0.00051 sec    | 0.00279 sec   |
| 10 개            | 0.03467 sec     | 0.07546 sec   | 0.01188 sec    | 0.09655 sec   |
| 100 개           | 0.28960 sec     | 0.70480 sec   | 0.09319 sec    | 0.72207 sec   |
| 1000 개          | 2.59061 sec     | 6.38031 sec   | 0.94029 sec    | 6.46660 sec   |
| 10000 개         | 27.61180 sec     | 77.73616 sec   | 11.43677 sec    | 68.20249 sec   |
| 100000 개        | 262.72305 sec     | 699.70416 sec   | 95.79926 sec    | 672.83272 sec   |

위는 데이터 개수를 증가하면서 pynori를 포함한 다양한 종류의 한국어 형태소 분석기의 처리 속도를 나타낸 표입니다 (참고 ./tests/test_compare_morphs.ipynb). 비교 대상은 모두 파이썬 라이브러리(konlpy)에 모두 속해 있지만 내부적으로 JVM 기반으로 동작합니다. 반면, Pynori는 순수 파이썬 스크립트로 실행됩니다. 그럼에도 트위터를 제외하고는 큰 차이가 발생하지 않습니다.

## Release History

|                 | 내용      |
| :-------------: | :-------------: |
| pynori 0.1.0    | 기본적인 노리 파이썬 패키지 & & 유닛테스트 구현 완료 (초기 버전) | 
| pynori 0.1.1    | KoreanAnalyzer 초기화 속도 향상 (1min 15s -> 12.9 s)     | 


## License

* Apache License 2.0

## Reference
* (Github) [Lucene-solr - Nori](https://github.com/apache/lucene-solr/tree/master/lucene/analysis/nori)
* (Github) [Mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/)
* (Blog) [엘라스틱서치 공식 한국어 분석 플러그인 '노리'](https://www.elastic.co/kr/blog/nori-the-official-elasticsearch-plugin-for-korean-language-analysis)
* (Blog) [노리(Nori) 형태소 분석기 Deep Dive](https://gritmind.github.io/2019/05/nori-deep-dive.html)
