<template>
 <div>
  <h1>{{
    message.split('').reverse().join('') 
    }}</h1>
 </div>
 <div>
  <a :href="url">点我</a>
 </div>
 <div>
  <p v-if="isVisible">这段文字是可见的</p>
  <button @click="AboutVisibility">切换可见性</button>
 </div>
 <div>
  <ul>
   <li v-for="item in items" :key="item.id">{{ item.toolsname }}</li>
  </ul>
 </div>
 <div>
  <input v-model="msg" placeholder="输入内容"/>
  <p>{{ msg }}</p>
 </div>
 <div>
  <button @click="increment">点击我</button>
  <p>点击次数: {{ count }}</p>
 </div>
 <div>
  
  <p>原始金额:<input type="text" v-model="originalAmount"></p>
  <p>税后金额：{{ taxAmount }}</p>
 </div>
 <div>
  <input type="text" v-model="message">
  <p>{{ message }}</p>
 </div>
 <div>
  <img :src="imgUrl" alt="?">
 </div>
 <div>
  <p v-if="showit">Hello Vue!</p>
  <p v-else>Goodbye Vue!</p>
  <button @click="showit = !showit">切换</button>
 </div>
 <div id="lightDiv">
  <div v-show="lightOn">
<img src="https://vuejs.org/images/logo.png" alt="?">
 </div>
 <button @click="lightOn = !lightOn">切换灯光</button>
  </div>
  <div>
    <button @click="showit = !showit">显示/隐藏</button>
    <p v-show="showit">hello Vue</p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String,
    originalAmount: Number
  },
  data() {
    return {
      imgUrl: 'https://vuejs.org/images/logo.png',  
      message: 'Hello!',
      msg: '',
      count: 0,
      originalAmount: 0,
      lightOn:true,
      url: 'https://www.baidu.com',
      isVisible: true,
      showit:true,
      items:[
        {id:1,toolsname:"Vue3"},
        {id:2,toolsname:"React"},
        {id:3,toolsname:"Angular"}
      ]
    };
  },
  methods:{
    AboutVisibility(){
      this.isVisible = !this.isVisible;
    },
    increment(){
      this.count++;
    },

  },
  computed:{
    taxAmount(){
      return this.originalAmount * 1.1;
    }
  }

};
</script>
