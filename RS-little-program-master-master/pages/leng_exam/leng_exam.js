var app = getApp();
Page({
  data: {
    index: 0,  // 题目序列
    chooseValue: [], // 选择的答案序列
    totalScore: 100, // 总分
    wrong: 0, // 错误的题目数量
    result:[],//结果 
    // wrongList: [], // 错误的题目集合
    wrongListSort: [], //错误的题目集合-正序

  },

  onLoad: function (options) {
    console.log(options);
    wx.setNavigationBarTitle({ title: "冷启动模式" }) // 动态设置导航条标题

    this.setData({
      questionList: app.globalData.questionList  // 拿到答题数据
      // testId: options.testId // 课程ID
    })
    console.log(this.data.questionList); 
    let count = this.generateArray(0, this.data.questionList.length-1); // 生成题序
    console.log("count:",count); 
  },
  /*
  * 单选事件
  */
  radioChange: function (e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    this.data.chooseValue[this.data.index] = e.detail.value;
    console.log(this.data.chooseValue);
  }, 
  /*
  * 退出答题 按钮
  */
  outTest: function(){
    wx.showModal({
      title: '提示',
      content: '本次做题结果将不会被保存，你真的要退出答题吗？',
      success(res) {
        if (res.confirm) {
          console.log('用户点击确定')
          wx.switchTab({
            url: '../home/home'
          })
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
   /*
  * 下一题/提交 按钮
  */
 nextSubmit: function () {
  // 如果没有选择
  if (this.data.chooseValue[this.data.index] == undefined || this.data.chooseValue[this.data.index].length == 0) {
    wx.showToast({
      title: '请选择至少一个答案!',
      icon: 'none',
      duration: 2000,
      success: function () {
        return;
      }
    })
    return;
  }

  // 判断答案是否正确
  this.chooseError();

  // 判断是不是最后一题
  if (this.data.index < this.data.questionList.length - 1) {
    // 渲染下一题
    this.setData({
      index: this.data.index + 1
    })
  } 
  else {
    wx.request({
      url: 'http://8.210.20.160:5000/user/record',
      method: "POST",
      data: {  
        username: app.globalData.username,
        examname:app.globalData.isleng
      }, 
      success: function(res)
      { 
        console.log(res.data); 
        if(res.data.code==400)
        { 
          wx.showToast({
            title: '错误',
            icon: 'none',
            duration: 2000  //持续的时间
          })
        }
        else
        {     
          console.log("记录插入成功");
        }
      }
    })
    wx.request({
      url: 'http://8.210.20.160:5000/user/result',
      method: "POST",
      data: {  
        username: app.globalData.username,
        result: this.data.result,
        examname: app.globalData.isleng,
        date: Date.now(),
        score: this.data.totalScore
      }, 
      success: function(res)
      { 
        console.log(res.data); 
        if(res.data.code==400)
        { 
          wx.showToast({
            title: '错误',
            icon: 'none',
            duration: 2000  //持续的时间
          })
        }
        else
        {     
          console.log("成绩插入成功");
        }
      }
    })
    let wrongListSort = JSON.stringify(this.data.wrongListSort);
    let chooseValue = JSON.stringify(this.data.chooseValue);
    wx.navigateTo({
      url: '../results/results?totalScore=' + this.data.totalScore + '&chooseValue=' + chooseValue + '&wrongListSort=' + wrongListSort 
    })

    // 设置缓存
    var logs = wx.getStorageSync('logs') || []
    let logsList = { "date": Date.now(),   "testId": '冷启动模式',"score": this.data.totalScore }
    logs.unshift(logsList);
    wx.setStorageSync('logs', logs);
  }
 },
 /*
  * 上一题 按钮
  */
 lastSubmit: function () {
  // 判断是不是第一题
  if (this.data.index >0) {
    // 渲染上一题
    this.setData({
      index: this.data.index - 1
    })
  }
},
  /*
  * 错题处理
  */
  chooseError: function(){
    var trueValue = this.data.questionList[this.data.index]['true'];
    var chooseVal = this.data.chooseValue[this.data.index];
    console.log('选择了' + chooseVal + '答案是' + trueValue);
    if (chooseVal.toString() != trueValue.toString()) {
      console.log('错了');
      this.data.result[this.data.index] = -1;
      this.data.wrong++;
      this.data.wrongListSort.push(this.data.index);
      this.setData({
        totalScore: this.data.totalScore - this.data.questionList[this.data.index]['scores']  // 扣分操作
      })
    }
    else{
      this.data.result[this.data.index] = 1;
    }
  },
  /**
     * 生成一个从 start 到 end 的连续数组
     * @param start
     * @param end
     */
   generateArray: function(start, end) {
    return Array.from(new Array(end + 1).keys()).slice(start)
  }
  
})
 