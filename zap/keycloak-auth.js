function authenticate(helper, paramsValues, credentials) {
    var requestUri = paramsValues.get("loginPageUrl");

    var requestBody =
        "client_id=" + encodeURIComponent(paramsValues.get("client_id")) +
        "&client_secret=" + encodeURIComponent(paramsValues.get("client_secret")) +
        "&grant_type=password" +
        "&username=" + encodeURIComponent(credentials.getParam("username")) +
        "&password=" + encodeURIComponent(credentials.getParam("password"));

    var msg = helper.prepareMessage();

    msg.getRequestHeader().setURI(
        new org.apache.commons.httpclient.URI(requestUri, false)
    );

    msg.getRequestHeader().setMethod("POST");
    msg.getRequestHeader().setHeader(
        "Content-Type",
        "application/x-www-form-urlencoded"
    );

    msg.setRequestBody(requestBody);
    msg.getRequestHeader().setContentLength(
        msg.getRequestBody().length()
    );

    helper.sendAndReceive(msg);

    return msg;
}