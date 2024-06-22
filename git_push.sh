#!/bin/sh

# 커밋 메시지를 인자로 받음
COMMIT_MESSAGE=$1

# 변경 사항 추가
git add .

# 커밋 (empty commit도 허용)
git commit --allow-empty -m "$COMMIT_MESSAGE"

# 원격 저장소에 푸시
git push
