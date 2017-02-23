package com.milo.ironwill.keepmydevices;

/**
 * Created by Milo on 16/8/17.
 */
public interface IMainView {

    void showLastMessage(String message);
    void initClockButton();
    void showClockResult(String result);
    void setMapPosition(double latitude, double longitude);
}
