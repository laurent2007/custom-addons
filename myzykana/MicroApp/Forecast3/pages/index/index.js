//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    update: '',
    basic: {},
    today: {},
    tomorrow: {},
    afterTomor: {},
    todayIcon: '../../imgs/weather/cond_icon-999.png',
    tomorrowIcon: '../../imgs/weather/cond_icon-999.png',
    afterTomorIcon: '../../imgs/weather/cond_icon-999.png',
    lifestyle:{}
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onShow: function () {
    console.log("t");
    this.getLocation();
  },
  onLoad: function () {

  },

  getLocation: function () {
    var that = this;
    wx.getLocation({
      type: 'wgs84',
      success: function (res) {
        var latitude = res.latitude;
        var longitude = res.longitude;
        that.getWeather(latitude, longitude);
      },
    })
  },
  getWeather: function (latitude, longitude) {
    //console.log(latitude);
    //console.log(longitude);
    var _this = this;
    var key = '955589446c684420b05f9b08cc860521';
    var url = 'https://free-api.heweather.com/s6/weather?key=' + key + '&location=' + longitude + ',' + latitude;
    //console.log(url);
    wx.request({
      url: url,
      data: {},
      method: 'GET',
      success: function (res) {
        var daily_forecast_today = res.data.HeWeather6[0].daily_forecast[0];
        var daily_forecast_tomorrow = res.data.HeWeather6[0].daily_forecast[1];
        var daily_forecast_afterTomor = res.data.HeWeather6[0].daily_forecast[2];

        var basic = res.data.HeWeather6[0].basic;
        var update = res.data.HeWeather6[0].update.loc;
        var lifestyle = res.data.HeWeather6[0].lifestyle;

        _this.setData({
          update: update,
          basic: basic,
          today: daily_forecast_today,
          tomorrow: daily_forecast_tomorrow,
          afterTomor: daily_forecast_afterTomor,
          todayIcon: '../../imgs/weather/cond_icon-' + daily_forecast_today.cond_code_d + '.png', //在和风天气中下载天气的icon图标，根据cond_code_d显示相应的图标
          tomorrowIcon: '../../imgs/weather/cond_icon-' + daily_forecast_tomorrow.cond_code_d + '.png',
          afterTomorIcon: '../../imgs/weather/cond_icon-' + daily_forecast_afterTomor.cond_code_d + '.png',
          lifestyle:lifestyle
        });

        //console.log(daily_forecast_today.cond_code_d);
      },
    })
  },
})