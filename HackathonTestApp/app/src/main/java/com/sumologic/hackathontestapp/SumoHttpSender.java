package com.sumologic.hackathontestapp;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

import okhttp3.Headers;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class SumoHttpSender {
    private Logger log = LoggerFactory.getLogger("sumo-http-sender");
    private OkHttpClient client = new OkHttpClient();

    private static final String SUMO_SOURCE_NAME_HEADER = "X-Sumo-Name";
    private static final String SUMO_SOURCE_CATEGORY_HEADER = "X-Sumo-Category";
    private static final String SUMO_SOURCE_HOST_HEADER = "X-Sumo-Host";
    private static final String SUMO_CLIENT_HEADER = "X-Sumo-Client";

    private static final String SUMO_CLIENT_HEADER_VALUE = "android-appender";

    private long retryInterval = 10000L;
    private int connectionTimeout = 1000;
    private int socketTimeout = 60000;
    private String url = null;
    private String sourceName = null;
    private String sourceCategory = null;
    private String sourceHost = null;


    public void setRetryInterval(long retryInterval) {
        this.retryInterval = retryInterval;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public void setSourceName(String sourceName) {
        this.sourceName = sourceName;
    }

    public void setSourceCategory(String sourceCategory) {
        this.sourceCategory = sourceCategory;
    }

    public void setSourceHost(String sourceHost) {
        this.sourceHost = sourceHost;
    }

    public void setConnectionTimeout(int connectionTimeout) {
        this.connectionTimeout = connectionTimeout;
    }

    public void setSocketTimeout(int socketTimeout) {
        this.socketTimeout = socketTimeout;
    }

    public void testSend(String data, String url) {
        RequestBody body = RequestBody.create(null,  data);
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();

        try {
            log.debug("Sending http request", request.headers().toString());
            try (Response response = client.newCall(request).execute()) {
                if (!response.isSuccessful())
                    log.debug("Error while sending http request" + response.toString());

                log.info(String.valueOf(response.code()));
                Headers responseHeaders = response.headers();
                for (int i = 0; i < responseHeaders.size(); i++) {
                    log.debug(responseHeaders.name(i) + ": " + responseHeaders.value(i));
                }
                log.debug(response.body().string());
            }
        } catch (IOException e) {
            log.error(e.toString());
        }
    }

    public void send(String body) {
        keepTrying(body);
    }

    private void keepTrying(String body) {
        boolean success = false;
        do {
            try {
                trySend(body);
                success = true;
            } catch (Exception e) {
                try {
                    Thread.sleep(retryInterval);
                } catch (InterruptedException e1) {
                    break;
                }
            }
        } while (!success && !Thread.currentThread().isInterrupted());
    }


    private void trySend(String body) throws IOException {
        Request.Builder reqBuilder = new Request.Builder(); //.build();
        if (url == null)
            throw new IOException("Unknown endpoint");

        reqBuilder.url(url);
        safeSetHeader(reqBuilder, SUMO_SOURCE_NAME_HEADER, sourceName);
        safeSetHeader(reqBuilder, SUMO_SOURCE_CATEGORY_HEADER, sourceCategory);
        safeSetHeader(reqBuilder, SUMO_SOURCE_HOST_HEADER, sourceHost);
        safeSetHeader(reqBuilder, SUMO_CLIENT_HEADER, SUMO_CLIENT_HEADER_VALUE);
        //reqBuilder.setEntity(new StringEntity(body, Consts.UTF_8));
        RequestBody reqBody = RequestBody.create(
                MediaType.parse("text/plain; charset=utf-8"), body);
        reqBuilder.post(reqBody);
        Request req = reqBuilder.build();

        try {
            try (Response response = client.newCall(req).execute()) {
                if (!response.isSuccessful())
                    log.debug("Error while sending http request" + response.toString());

                if (response.code() != 200) {
                    log.warn("Received HTTP error from Sumo Service: %d", response.code());
                    // Not success. Only retry if status is unavailable.
                    if (response.code() == 503) {
                        throw new IOException("Server unavailable");
                    }
                }

                //need to consume the body if you want to re-use the connection.
                log.debug("Successfully sent log request to Sumo Logic");
                Headers responseHeaders = response.headers();
                for (int i = 0; i < responseHeaders.size(); i++) {
                    log.debug(responseHeaders.name(i) + ": " + responseHeaders.value(i));
                }
                log.debug(response.body().string());
            }
        } catch (IOException e) {
            log.warn("Could not send log to Sumo Logic");
            log.debug("Reason:", e);
        }
    }

    private void safeSetHeader(Request.Builder request, String name, String value) {
        if (value != null && !value.trim().isEmpty()) {
            request.header(name, value);
        }
    }
}