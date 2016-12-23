package com.milo.ironwill.keepmydevices;

import android.location.Location;

import java.util.Date;

/**
 * Created by Milo on 16/8/18.
 */
public class Device {
    private String deviceBrand;
    private String deviceModel;

    private double deviceLatitude;
    private double deviceLongitude;

    public Device(String brand, String model, Location location) {
        deviceBrand     = brand;
        deviceModel     = model;
        if (null != location) {
            deviceLatitude = location.getLatitude();
            deviceLongitude = location.getLongitude();
        } else {
            deviceLatitude = Double.valueOf("38.889");
            deviceLongitude = Double.valueOf("121.541");
        }
    }

    public String getDeviceBrand() {
        return  deviceBrand;
    }

    public String getDeviceModel() {
        return deviceModel;
    }

    public Double getDeviceLatitude() {
        return deviceLatitude;
    }

    public Double getDeviceLongitude() {
        return deviceLongitude;
    }

    public Date getTimeStamp() {
        return new Date();
    }
}
