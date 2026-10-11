<template>
  <div class="card" style="min-height: 80vh">

    <!-- 排序切换（首页/搜索列表） -->
    <div v-if="!type && total > 0" class="sort-bar">
      <span class="sort-label">排序：</span>
      <span class="sort-btn" :class="{active: sort==='composite'}" @click="changeSort('composite')">综合</span>
      <span class="sort-btn" :class="{active: sort==='date'}" @click="changeSort('date')">最新</span>
      <span class="sort-btn" :class="{active: sort==='reads'}" @click="changeSort('reads')">最热</span>
      <span class="sort-btn" :class="{active: sort==='likes'}" @click="changeSort('likes')">点赞最多</span>
    </div>

    <div class="blog-box" v-for="item in tableData" :key="item.id" v-if="total>0">

      <div style="flex: 1;width: 0">
        <!--标题-->
        <a :href="'/front/blogDetail?blogId='+item.id" target="_blank">
          <div class="line1 blog-title">
            <el-tag v-if="item.top === 1" type="danger" size="mini" style="margin-right: 6px">置顶</el-tag>
            {{ item.title }}
          </div>
        </a>
        <!--简介-->
        <div class="line1" style="font-size: 13px;margin-top: 5px;color: #515151;margin-right: 5px">
          {{ item.descr }}
        </div>

        <div style="display: flex;align-items: center">
          <div style="flex:1;font-size: 13px">
                <span style="color: #666666;margin-right: 10px">
                  <i class="el-icon-user" style="margin-right: 3px"></i>{{ item.userName }}
                </span>
            <span style="color: #666666;margin-right: 10px">
                  <i class="el-icon-eye" style="margin-right: 3px"></i>{{ item.readCount }}  <!--浏览量-->
                </span>
            <span style="color: #666666;margin-right: 10px">
                  <i class="el-icon-dianzan" style="margin-right: 3px"></i>{{ item.likesCount }}
                </span>
            <span v-if="showOpt" style="margin-left: 40px;color: red;cursor: pointer" @click="del(item.id)"><i class="el-icon-delete"></i>删除</span>
            <span v-if="showOpt" style="margin-left: 15px;color: #2a60c9;cursor: pointer" @click="editBlog(item.id)"><i class="el-icon-edit"></i>编辑</span>
          </div>
          <div style="width: fit-content">
            <el-tag v-for="item in JSON.parse(item.tags||'[]')" :key="item" type="primary"
                    style="margin-right:5px">
              {{ item }}
            </el-tag>
          </div>
        </div>

      </div>

      <!--封面-->
      <div style="width: 150px">
        <img style="width: 100%;height:80px;border-radius: 5px" :src="item.cover" alt="">
      </div>

    </div>

    <div  v-if="total===0" style="padding: 20px; text-align: center;font-size: 16px;color: #666666">
      暂无数据。
    </div>

    <div style="margin-top: 10px" v-if="total">
      <el-pagination
          background
          @current-change="handleCurrentChange"
          :current-page="pageNum"
          :page-sizes="[5, 10, 20]"
          :page-size="pageSize"
          layout="total, prev, pager, next"
          :total="total">
      </el-pagination>
    </div>

  </div>
</template>

<script>
export default {
  name: "BlogList",
  props: {
    categoryName: null,
    type:null,
    showOpt:false
  },
  data() {
    return {
      tableData: [],  // 所有的数据
      pageNum: 1,   // 当前的页码
      pageSize: 10,  // 每页显示的个数
      total: 0,     // 总记录数
      sort: 'composite', // 排序方式：composite综合 date最新 reads最热 likes点赞最多
    }
  },
  watch: {  // 监听数据变化  加载最新数据
    categoryName() {
      this.loadBlogs(1)
    }
  },
  created() {
    this.loadBlogs(1)
  },
  methods: {
    changeSort(sort) {   // 切换排序方式
      if (this.sort === sort) return
      this.sort = sort
      this.loadBlogs(1)
    },
    editBlog(blogId){
      window.open('/front/newBlog?blogId='+blogId)
    },
    del(id) {   // 单个删除
      this.$confirm('您确定删除吗？', '确认删除', {type: "warning"}).then(response => {
        this.$request.delete('/blog/delete/' + id).then(res => {
          if (res.code === '200') {   // 表示操作成功
            this.$message.success('操作成功')
            this.loadBlogs(1)
          } else {
            this.$message.error(res.msg)  // 弹出错误的信息
          }
        })
      }).catch(() => {
      })
    },
    loadBlogs(pageNumber) {  //博客分页
      //请求博客数据
      if (pageNumber) this.pageNum = pageNumber

      let url
      switch (this.type){
        case 'user': url = '/blog/selectUserBlog';break;
        case 'like': url = '/blog/selectUserLike';break;
        case 'collect': url = '/blog/selectUserCollect';break;
        case 'comment': url = '/blog/selectUserComment';break;
        default:url='/blog/selectPage' //默认 查全部
      }
      this.$request.get(url, {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          categoryName: this.categoryName === '全部博客' ? null : this.categoryName,
          title:this.$route.query.title,
          sort: this.type ? null : this.sort
        }
      }).then(res => {
        this.tableData = res.data?.list
        this.total = res.data?.total
      })
    },
    handleCurrentChange(pageNum) {//翻页
      this.loadBlogs(pageNum)
    },
  }
}
</script>

<style>

.blog-box {
  display: flex;
  grid-gap: 15px;
  padding: 10px 0;
  border-bottom: 1px solid #dddddd;
}

.blog-box:first-child {
  padding-top: 0;
}

.blog-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  margin-right: 5px;
  cursor: pointer;
}

.blog-title:hover {
  color: #2a60c9;
}

/* 排序切换 */
.sort-bar {
  display: flex;
  align-items: center;
  padding: 5px 5px 12px;
  border-bottom: 1px solid #dddddd;
}
.sort-label {
  font-size: 13px;
  color: #909399;
  margin-right: 8px;
}
.sort-btn {
  padding: 4px 14px;
  margin-right: 8px;
  font-size: 13px;
  color: #666666;
  background: #f4f4f5;
  border-radius: 4px;
  cursor: pointer;
  transition: all .2s;
}
.sort-btn:hover {
  color: #1890ff;
}
.sort-btn.active {
  color: #ffffff;
  background-color: #1890ff;
}
</style>