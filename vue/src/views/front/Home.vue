<template>
  <div class="main-content">
    <div style="display: flex;align-items: flex-start;grid-gap: 10px">

      <!--左边分类模块-->
      <div style="width: 150px" class="card">
        <div class="category-item" :class="{'category-item-active': item.name===current}" v-for="item in categoryList"
             :key="item.id" @click="selectCategory(item.name)"> {{ item.name }}
        </div>
      </div>

      <!--中间博客展示模块-->
      <div style="flex: 1">

        <BlogList :categoryName="current"/>

        <Footer/>

      </div>

      <!--右边-->
      <div style="width: 260px">
        <div class="card" style="margin-bottom: 10px">
          <div style="font-size: 20px;font-weight: bold;margin-bottom: 10px">
            欢迎您！😊
          </div>
          <a href="/front/person">
            <div style="color: #666666">写下博客，记录美好的一天！</div>
          </a>
        </div>

        <!--榜单模块-->
        <div class="card" style="margin-bottom: 10px">
          <div style="display: flex;align-items:center;padding-bottom: 10px;border-bottom: 1px solid #dddddd">
            <div style="font-size: 20px;flex: 1">IT技术文章热榜</div>
            <div style="font-size: 12px;color: #666666;cursor: pointer;" @click="refreshTop"><i
                class="el-icon-refresh"></i>换一换
            </div>
          </div>

          <div>
            <div v-for="item in showList" :key="item.id" style="margin: 15px 0" class="line1">
              <a :href="'/front/blogDetail?blogId='+item.id" target="_blank">
              <span style="width: 18px;display:inline-block;text-align: right;margin-right: 10px">
                    <span style="color: orangered" v-if="item.index===1">{{ item.index }}</span>
                    <span style="color: goldenrod" v-else-if="item.index===2">{{ item.index }}</span>
                    <span style="color: dodgerblue" v-else-if="item.index===3">{{ item.index }}</span>
                    <span style="color: #87724d" v-else>{{ item.index }}</span>
              </span>

                <span style="color: #666666">{{ item.title }}</span>
              </a>
            </div>

          </div>

        </div>

        <div style="margin-bottom: 10px">
          <div v-for="item in topActivityList" :key="item.id" style="margin-bottom: 10px">
            <a :href="'/front/activityDetail?activityId='+item.id" target="_blank">
              <img :src="item.cover" alt="" style="width:100%;border-radius: 5px">
            </a>
          </div>
        </div>

        <div style="line-height: 30px; color: #666; padding: 0 10px">
          <div> 举报邮箱： feedback@outlook.io</div>
          <div> 座机电话： M78%$%@%%$%$*&</div>
          <div> 宇宙警ICP备888888©2025 Captain_dong</div>
        </div>

      </div>

    </div>
  </div>
</template>

<script>

import Footer from "@/components/Footer.vue";
import BlogList from "@/components/BlogList.vue";

export default {
  components: {
    BlogList,
    Footer
  },

  data() {
    return {
      current: '全部博客',
      categoryList: [],
      topList: [],
      showList: [],
      lastIndex: 0,
      topActivityList: []
    }
  },
  mounted() {
    this.load()

    this.refreshTop()

    this.loadTopActivity()
  },
  // methods：本页面所有的点击事件或者其他函数定义区
  methods: {
    loadTopActivity() {
      this.$request.get('/activity/selectTop').then(res => {
        this.topActivityList = res.data || []
      })
    },
    refreshTop() {
      this.$request.get('/blog/selectTop').then(res => {
        this.topList = res.data || []
        this.topList = res.data || []
        let i = 1
        this.topList.forEach(item => item.index = i++)

        if (this.lastIndex === 20) {
          this.lastIndex = 0;
        }
        this.showList = this.topList.slice(this.lastIndex, this.lastIndex + 5)
        this.lastIndex += 5;
      })
    },
    //切换分类
    selectCategory(categoryName) {
      this.current = categoryName
    },
    load() {
      //请求分类的数据
      this.$request.get('/category/selectAll').then(res => {
        this.categoryList = res.data || []
        this.categoryList.unshift({name: '全部博客', id: 0})
      })
    },

  }
}
</script>
<style>
/* 分类胶囊样式已统一移至 front.css（.main-body .category-item） */
</style>