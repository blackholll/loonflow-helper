import requests
from apps.ticket.models import TicketRecord
from service.ticket.ticket_base_service import TicketBaseService


def demo_script_call():
    # ticket_id will passed by globals， you can get ticket info by TicketBaseService.get_ticket_field_value with 'ticket_id' arg
    username, msg = TicketBaseService.get_ticket_field_value(ticket_id, 'creator')  # ticket_id会通过exec传过来
    host_name, msg2 = TicketBaseService.get_ticket_field_value(ticket_id, 'host_name') 
    if (username and host_name):   
        # then you can call your own api to create vm
        post_data = dict(username=username, host_name=host_name)
        resp = requests.post('http://xxxx.com/api/v1.0/vms', json=post_data).json()
        if resp.code == 0:
            host_ip = resp.data.get('host_ip', '')
            # print msg will saved by loonflow in ticket_flow_log record
            print('host_ip is {}'.format(host_ip))
            return True, ''
        else:
            raise Exception('create vm fail: {}'.format(resp.msg))
    else:
        raise Exception('get ticket info fail, username:{}, host_name:{}'.format(msg, msg2))
    return True, ''


demo_script_call()