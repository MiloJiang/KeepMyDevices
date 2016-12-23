package com.milo.ironwill.keepmydevices;

import android.location.Location;
import android.os.Build;

import com.wilddog.client.DataSnapshot;
import com.wilddog.client.Query;
import com.wilddog.client.ValueEventListener;
import com.wilddog.client.Wilddog;
import com.wilddog.client.WilddogError;

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
    private Wilddog mDevices;
    private Location mLocation;

    public MainPresenter(IMainView view) {
        mView = view;
    }

    public void setLocation(Location location) {
        mLocation = location;
    }

    private Wilddog getDog() {
        if (mDevices == null) {
            mDevices = new Wilddog("https://kanban.wilddogio.com/devices");
        }
        return mDevices;
    }


    public void addDevice() {
        Device device = new Device(Build.BRAND, Build.MODEL, mLocation);
        getDog().child(Build.SERIAL).setValue(device, new Wilddog.CompletionListener() {
            @Override
            public void onComplete(WilddogError wilddogError, Wilddog wilddog) {
                String ret;
                if (wilddogError != null) {
                    ret = DATA_ERROR + wilddogError.getMessage();
                } else {
                    ret = DATA_SUCCESS;
                    updateLastRecord();
                }
                mView.showClockResult(ret);
            }
        });
    }

    public void searchDevice() {

    }

    public void updateLastRecord() {
        Query queryRef = getDog().child(Build.SERIAL);
        queryRef.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot snapshot) {
                Date timestamp = new Date((Long) snapshot.child(DEVICE_TIME_STAMP).getValue());
                SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.CHINA);
                mView.showLastMessage(LAST_MESSAGE + format.format(timestamp));

                double deviceLatitude = (double) snapshot.child(DEVICE_LATITUDE).getValue();
                double deviceLongitude = (double) snapshot.child(DEVICE_LONGITUDE).getValue();
                mView.setMapPosition(deviceLatitude, deviceLongitude);
            }

            @Override
            public void onCancelled(WilddogError error) {

            }
        });
    }
}
