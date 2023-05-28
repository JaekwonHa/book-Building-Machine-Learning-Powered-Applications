# 머신러닝 파워드 애플리케이션
![cover](assets/cover.jpeg){width="500" height="700"}

> git: https://github.com/rickiepark/ml-powered-applications




## 1장. 제품의 목표를 머신러닝 문제로 표현하기

어떤 문제를 해결할 것인가?
어떤 모델을 사용할 것인가?
데이터셋 구성하기

가장 간단한 모델부터 시작하기
알고리즘이 되어보기


## 2장. 계획 수립하기

성공을 측정하는 방법 정하기
간단한 파이프라인으로 시작하기

훈련 / 추론 파이프라인

## 3장. 엔드투엔드 파이프라인 만들기

머신러닝 에디터 프로토타입 만들기

최초 머신러닝 에디터 프로토타입은 모델을 사용하지 않는다
질문을 전처리하고 다양한 기준으로 평가해본다

* 전처리
	- 텍스트를 토큰화
* 품질 평가
	- 자주 사용하는 동사와 연결어의 빈도를 카운트
	- wh- 접속사를 카운트
	- 플레시 Flesch 가독성 점수를 계산


```bash
❯ python ch3.ml-editor.py "Is this workflow any good?"
단어 사용량: 0 told/said, 0 but/and, 0 wh- 접속사<br/>단어의 평균 길이 3.67, 고유한 단어의 비율 1.00<br/>6개 음절, 5개 단어, 1개 문장<br/>플레시 점수 100.26: 매우 읽기 쉬움

❯ python ch3.ml-editor.py "Here is a needlessly obscure question, that dose not provide clearly which information it would like to acquire, does it?"
단어 사용량: 0 told/said, 0 but/and, 0 wh- 접속사<br/>단어의 평균 길이 4.43, 고유한 단어의 비율 0.91<br/>30개 음절, 20개 단어, 1개 문장<br/>플레시 점수 59.65: 약간 읽기 어려움
```

반환된 정보가 너무 장황하고 관련성이 낮다
점수 대신 실행 가능한 추천을 해주는 것이 좋다


































