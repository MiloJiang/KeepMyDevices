package com.milo.ironwill.keepmydevices;

import android.location.Location;

/**
 * Created by Milo on 16/8/18.
 */
public class Device {
    private String deviceSN;
    private String deviceBrand;
    private String deviceModel;

    private double deviceLatitude;
    private double deviceLongitude;

    public Device(String sn, String brand, String model, Location location) {
        deviceSN        = sn;
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

    public String string() {
        String result = "{" + String.format("\"%s\": \"%s\",", "sn", deviceSN) +
                String.format("\"%s\": \"%s\",", "brand", deviceBrand) +
                String.format("\"%s\": \"%s\",", "model", deviceModel) +
                String.format("\"%s\": \"%s\",", "latitude", deviceLatitude) +
                String.format("\"%s\": \"%s\"", "longitude", deviceLongitude) +
                "}";
        return result;
    }
}
