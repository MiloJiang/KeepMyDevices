package com.milo.ironwill.keepmydevices;

import java.io.IOException;

import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.Response;
import com.squareup.okhttp.MediaType;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Callback;

import org.json.JSONObject;
import org.json.JSONException;


/**
 * Created by jianglei on 2017/2/21.
 */
public class ServerHandler {
    public static final MediaType JSON
            = MediaType.parse("application/json; charset=utf-8");

    private static final String URL_BASE = "http://10.0.2.1:5000";
    private static final String URL_AUTH = URL_BASE + "/auth";
    private static final String URL_DEVICE = URL_BASE + "/api/v1/update";

    OkHttpClient client = new OkHttpClient();
    MainPresenter mainPresenter = null;

    public ServerHandler(MainPresenter presenter) {
        mainPresenter = presenter;
    }

    private String mToken = "";
    private int mStatus = 0;

    public void init() {
        mStatus = 0;
        mToken = "";
        getToken();
    }


    protected void getToken() {
        String payload = "{\"username\":\"admin\",\"password\":\"admin\"}";
        RequestBody body = RequestBody.create(JSON, payload);
        Request request = new Request.Builder()
                .url(URL_AUTH)
                .post(body)
                .build();
        client.newCall(request).enqueue(new Callback(){

            @Override
            public void onFailure(Request request, IOException e) {

            }

            @Override
            public void onResponse(Response response) throws IOException{
                mStatus -= 1;
                if (response.isSuccessful()) {
                    try {
                        JSONObject json = new JSONObject(response.body().string());
                        mToken = json.get("access_token").toString();
                    } catch (JSONException e) {
                        init();
                    }
                }
            }
        });
        mStatus += 1;
    }


    public void addDevice(String jsonInfo) {
        if (mStatus != 0 && mToken.isEmpty()) {
            mainPresenter.showFailure();
        } else {
            RequestBody body = RequestBody.create(JSON, jsonInfo);
            Request request = new Request.Builder()
                    .addHeader("Authorization", "JWT " + mToken)
                    .url(URL_DEVICE)
                    .post(body)
                    .build();
            client.newCall(request).enqueue(new Callback(){

                @Override
                public void onFailure(Request request, IOException e) {

                }

                @Override
                public void onResponse(Response response) throws IOException{
                    mStatus -= 1;
                    if (response.isSuccessful()) {
                        try {
                            JSONObject json = new JSONObject(response.body().string());
                            double latitude = json.getDouble("latitude");
                            double longitude = json.getDouble("longitude");
                            String timestamp = json.getString("timestamp");
                            mainPresenter.updateLastRecord(timestamp, latitude, longitude);
                            mainPresenter.showSuccess();
                        } catch (JSONException e) {
                            e.printStackTrace();
                            mainPresenter.showFailure();
                        }
                    }
                }
            });
        }
    }
}
