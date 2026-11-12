"""Protocol example. Replace respond() with your existing agent call. No API key needed."""
import json,sys
def respond(messages):
    return '제공된 자료에서 핵심 판단 기준과 이를 충족하는 근거를 먼저 확인해야 합니다.'
if __name__=='__main__':
    if hasattr(sys.stdin,'reconfigure'):sys.stdin.reconfigure(encoding='utf-8');sys.stdout.reconfigure(encoding='utf-8')
    request=json.load(sys.stdin)
    print(json.dumps({'response':respond(request['messages'])},ensure_ascii=False))
