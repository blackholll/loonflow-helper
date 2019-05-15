import requests

"""
globals = {'title_result': title_result, 'content_result': content_result,
                   'participant': ticket_obj.participant, 'participant_type_id': ticket_obj.participant_type_id,
                   'multi_all_person': ticket_obj.multi_all_person, 'ticket_value_info': ticket_value_info,
                   'last_flow_log': last_flow_log, 'participant_info_list': participant_info_list
           }
loonflow will pass some info by globals, so you can use this params directly，

"""

def demo_notice_script_call():
    phone_list = []
    email_list = []
    for participant_info in participant_info_list:
        phone_list.append(participant_info['phone'])
        # your company may provide sms api. you can use it directly
    resp = requests.post('http://xxxxx.com/sendsms', {'phone': phone_list, 'context': content_result})
    if resp.json().get('code') == 0:
        return True, ''
    else:
        raise Exception('send_sms_result fail:{}'.format(sms_result.json().get('msg')))


demo_notice_script_call()
