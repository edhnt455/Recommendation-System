// app.js
App({
  onLaunch() {
    
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })

    //获取屏幕高度
    var windowHeight = 0;
    wx.getSystemInfo({
      success: function (res) {
        windowHeight = res.windowHeight;
      }
    })
    this.globalData.windowHeight = windowHeight;

     // 获取系统状态栏信息
     wx.getSystemInfo({
      success: e => {
        this.globalData.StatusBar = e.statusBarHeight;
        let custom = wx.getMenuButtonBoundingClientRect();
        this.globalData.Custom = custom;
        this.globalData.CustomBar = custom.bottom + custom.top - e.statusBarHeight;
      }
    })
  },
  
  globalData: {
    questionList: null,  // 拿到答题数据
    ques_id: null,  //题目id
    username: null,  // 用户名
    userclass: null, //用户类型，1是已完成摸底测试，2是未完成
    isleng:null// true是冷启动，false是推荐模式
    
  }  
})
