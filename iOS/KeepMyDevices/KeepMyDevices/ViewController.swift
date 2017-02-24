//
//  ViewController.swift
//  KeepMyDevice
//
//  Created by jianglei on 2016/8/24.
//  Copyright © 2016年 jianglei. All rights reserved.
//

import UIKit
import CoreLocation
import MapKit
import Alamofire

extension UIDevice{
    ///设备型号的名称
    var modelName:String{
        var systemInfo = utsname()
        uname(&systemInfo)
        let machineMirror   = Mirror(reflecting: systemInfo.machine)
        let identifier      = machineMirror.children.reduce("") { identifier, element in
            guard let value = element.value as? Int8, value != 0 else { return identifier }
            return identifier + String(UnicodeScalar(UInt8(value)))
        }

        switch identifier {
        case"iPhone3,1","iPhone3,2","iPhone3,3"     :return"iPhone 4"

        case"iPhone4,1":return"iPhone 4s"

        case"iPhone5,1","iPhone5,2":return"iPhone 5"

        case"iPhone5,3","iPhone5,4":return"iPhone 5c"

        case"iPhone6,1","iPhone6,2":return"iPhone 5s"

        case"iPhone7,2":return"iPhone 6"

        case"iPhone7,1":return"iPhone 6 Plus"

        case"iPhone8,1":return"iPhone 6s"

        case"iPhone8,2":return"iPhone 6s Plus"

        case"iPad2,1","iPad2,2","iPad2,3","iPad2,4":return"iPad 2"

        case"iPad3,1","iPad3,2","iPad3,3":return"iPad 3"

        case"iPad3,4","iPad3,5","iPad3,6":return"iPad 4"

        case"iPad4,1","iPad4,2","iPad4,3":return"iPad Air"

        case"iPad5,3","iPad5,4":return"iPad Air 2"

        case"iPad2,5","iPad2,6","iPad2,7":return"iPad Mini"

        case"iPad4,4","iPad4,5","iPad4,6":return"iPad Mini 2"

        case"iPad4,7","iPad4,8","iPad4,9":return"iPad Mini 3"

        case"iPad5,1","iPad5,2":return"iPad Mini 4"

        case"iPad6,7","iPad6,8":return"iPad Pro"

        case"AppleTV5,3":return"Apple TV"

        case"i386","x86_64":return"Simulator"

        default: return identifier
        }
    }
}


class ViewController: UIViewController, CLLocationManagerDelegate {

    @IBOutlet weak var infoText: UILabel!;
    @IBOutlet weak var localMap: MKMapView!;

    var currentLocation: CLLocation?
    var currentAnnotation: MKPointAnnotation?
    var deviceInfo: Dictionary<String, String>?
    let locationManager: CLLocationManager = CLLocationManager()

    let baseURL: String = "http://127.0.0.1:5000"
    let authURL: String = "/auth"
    let updateURL: String = "/api/v1/update"
    let parameters: Parameters = ["username": "admin", "password": "admin"]

    var token: String = ""

    override func viewDidLoad() {
        super.viewDidLoad()

        locationManager.delegate        = self
        locationManager.distanceFilter  = kCLLocationAccuracyNearestTenMeters
        locationManager.desiredAccuracy = kCLLocationAccuracyBest

        Alamofire.request(baseURL+authURL,
                          method: .post,
                          parameters: parameters,
                          encoding: JSONEncoding.default)
            .validate().responseJSON { response in

                switch response.result {
                case .success:
                    NSLog("成功取得Token!")
                    if let tokenInfo = response.result.value {
                        let ret = tokenInfo as! Dictionary<String,String>
                        self.token = ret["access_token"]!
                    }
                case .failure(let error):
                    NSLog(error.localizedDescription)
                }
        }

        ////发送授权申请
        if #available(iOS 8.0, *) {
            locationManager.requestWhenInUseAuthorization()
        } else {
            // Fallback on earlier versions
        };
        if (CLLocationManager.locationServicesEnabled()) {
            //允许使用定位服务的话，开启定位服务更新
            locationManager.startUpdatingLocation()
            NSLog("定位开始")
        }

    }

    fileprivate func getPhoneInfo() {
        let idfv: String        = (UIDevice.current.identifierForVendor?.description)!
        let modelName:String    = UIDevice.current.modelName
        let latitude: Double    = (currentLocation?.coordinate.latitude)!
        let longitude: Double   = (currentLocation?.coordinate.longitude)!

        if (idfv.isEmpty || self.token.isEmpty) {
            return
        }

        let headers: HTTPHeaders = ["Authorization": "JWT " + token]
        let info: Dictionary<String, Any> = ["sn": idfv,
                                             "brand": "Apple",
                                             "model": modelName,
                                             "latitude": latitude,
                                             "longitude": longitude]

        Alamofire.request(self.baseURL+self.updateURL,
                          method: .post,
                          parameters: info,
                          encoding: JSONEncoding.default,
                          headers: headers)
            .validate().responseJSON { response in

                switch response.result {
                case .success:
                    NSLog("成功更新数据")
                    if let json = response.result.value {
                        let dict = json as! Dictionary<String,Any>
                        self.infoText.text = "打卡成功!: " + (dict["timestamp"] as! String)
                    }
                case .failure(let error):
                    NSLog(error.localizedDescription)
                }
        }
    }

    fileprivate func updateMapView(_ location: CLLocation) {
        //创建一个MKCoordinateSpan对象，设置地图的范围（越小越精确）
        let latDelta    = 0.005
        let longDelta   = 0.005
        let currentLocationSpan:MKCoordinateSpan    = MKCoordinateSpanMake(latDelta, longDelta)
        let currentRegion:MKCoordinateRegion        = MKCoordinateRegion(center: location.coordinate,
                                                                         span: currentLocationSpan)

        //设置显示区域
        self.localMap.setRegion(currentRegion, animated: true)

        if ((self.currentAnnotation) != nil) {
            self.localMap.removeAnnotation(currentAnnotation!)
        }

        //创建一个大头针对象
        currentAnnotation = MKPointAnnotation()
        //设置大头针的显示位置
        currentAnnotation?.coordinate = location.coordinate
        self.localMap.addAnnotation(currentAnnotation!)
    }


    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]){
        let location:CLLocation = locations[locations.count-1]

        if (location.horizontalAccuracy > 0) {
            self.locationManager.stopUpdatingLocation()
            currentLocation = location
            updateMapView(location)
        }
    }
//
//
//    fileprivate func getCurrentTime() -> String {
//        // 得到当前时间（世界标准时间 UTC/GMT）
//        var date:Date = Date()
//
//        // 设置系统时区为本地时区
//        let zone:TimeZone = TimeZone.current as TimeZone
//
//        // 计算本地时区与 GMT 时区的时间差
//        let second:Int = zone.secondsFromGMT()
//
//        // 在 GMT 时间基础上追加时间差值，得到本地时间
//        date = date.addingTimeInterval(TimeInterval(second))
//        return date.description
//    }

    @IBAction func handlePunch(_ sender: AnyObject) {
        getPhoneInfo()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}


