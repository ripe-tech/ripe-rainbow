def stringify_response_received(message_j):
    event = message_j["method"]
    request_id = message_j["params"]["requestId"]
    response = message_j["params"]["response"]
    url = response["url"]
    status = response["status"]
    headers = response["headers"]
    return '%s %s %s %s %s' % (event, request_id, status, url, headers)

def stringify_request_will_be_sent(message_j):
    event = message_j["method"]
    request_id = message_j["params"]["requestId"]
    request = message_j["params"]["request"]
    method = request["method"]
    url = request["url"]
    headers = request["headers"]
    return '%s %s %s %s %s' % (event, request_id, method, url, headers)

EVENT_STRINGIFIERS = {
    "Network.responseReceived": stringify_response_received,
    "Network.requestWillBeSent": stringify_request_will_be_sent
}
