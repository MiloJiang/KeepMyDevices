package com.milo.ironwill.keepmydevices;

import android.location.Location;
import android.os.Build;
import android.util.Log;

//import com.wilddog.client.DataSnapshot;
//import com.wilddog.client.Query;
//import com.wilddog.client.ValueEventListener;
//import com.wilddog.client.Wilddog;
//import com.wilddog.client.WilddogError;

import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * Created by Milo on 16/8/17.
 */
public class MainPresenter {

    private static final String DEVICE_TIME_STAMP = "timeStamp";
    private static final String DEVICE_LATITUDE = "deviceLatitude";
    private static final String DEVICE_LONGITUDE = "deviceLongitude";
    private static final String LAST_MESSAGE= "最后一次打卡时间为: ";

    private static final String DATA_SUCCESS = "设备打卡成功!";
    private static final String DATA_ERROR = "数据添加错误: ";

    private IMainView mView;
    private ServerHandler mDevices;
    private Location mLocation;

    public MainPresenter(IMainView view) {
        mView = view;
        getServer();
    }

    public void setLocation(Location location) {
        mLocation = location;
    }

    private ServerHandler getServer() {
        if (mDevices == null) {
            mDevices = new ServerHandler(this);
            mDevices.init();
        }
        return mDevices;
    }


    public void addDevice() {
        Device device = new Device(Build.SERIAL, Build.BRAND, Build.MODEL, mLocation);
        String info = device.string();
        mDevices.addDevice(info);
//        getDog().child(Build.SERIAL).setValue(device, new Wilddog.CompletionListener() {
//            @Override
//            public void onComplete(WilddogError wilddogError, Wilddog wilddog) {
//                String ret;
//                if (wilddogError != null) {
//                    ret = DATA_ERROR + wilddogError.getMessage();
//                } else {
//                    ret = DATA_SUCCESS;
//                    updateLastRecord();
//                }
//                mView.showClockResult(ret);
//            }
//        });
    }

    public void showSuccess() {
        mView.showClockResult(DATA_SUCCESS);
    }

    public void showFailure() {
        mView.showClockResult(DATA_ERROR);
    }

    public void updateLastRecord(final String timestamp, final double latitude, final double longitude) {
        ((MainActivity)mView).runOnUiThread(new Runnable() {
            @Override
            public void run() {
                mView.showLastMessage(LAST_MESSAGE + timestamp);
                mView.setMapPosition(latitude, longitude);
            }
        });
    }
}
