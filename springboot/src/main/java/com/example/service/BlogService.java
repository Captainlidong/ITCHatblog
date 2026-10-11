package com.example.service;

import cn.hutool.core.date.DateUtil;
import cn.hutool.core.util.ObjUtil;
import cn.hutool.json.JSONArray;
import cn.hutool.json.JSONUtil;
import com.example.common.enums.LikesModuleEnum;
import com.example.common.enums.RoleEnum;
import com.example.entity.*;
import com.example.mapper.BlogMapper;
import com.example.utils.TokenUtils;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * 功能：
 * 作者：captain_dong
 * 日期：2023/12/20 22:29
 */
@Service
public class BlogService {

    @Resource
    private BlogMapper blogMapper;//博客

    @Resource
    private  UserService userService;//用户

    @Resource
    private LikesService likesService; //点赞

    @Resource
    private CollectService collectService;//收藏
    /**
     * 新增
     * @param blog
     */
    public void add(Blog blog) {
        //设置发布日期为当前日期
        blog.setDate(DateUtil.today());

        //设置发布人--用户
        Account currentUser = TokenUtils.getCurrentUser();
        if (RoleEnum.USER.name().equals(currentUser.getRole())){
            blog.setUserId(currentUser.getId());
        }
        blogMapper.insert(blog);
    }

    /**
     * 删除
     * @param id
     */
    public void deleteById(Integer id) {
        blogMapper.deleteById(id);
    }

    /**
     * 批量删除
     * @param ids
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            blogMapper.deleteById(id);
        }
    }

    /**
     * 修改
     * @param blog
     */
    public void updateById(Blog blog) {
        blogMapper.updateById(blog);
    }

    /**
     * 根据ID查询
     * @param id
     * @return
     */
    public Blog selectById(Integer id) {
        Blog blog = blogMapper.selectById(id);
        User user = userService.selectById(blog.getUserId());
        List<Blog> userBlogList = blogMapper.selectUserBlog(user.getId());
        user.setBlogCount(userBlogList.size());  // 当前用户浏览的作者博客数量
        //  当前用户收到的点赞和收藏的数据
        int userLikesCount = 0;
        int userCollectCount = 0;
        for (Blog b : userBlogList) { // 遍历用户博客列表
            Integer fid = b.getId();
            int likesCount = likesService.selectByFidAndModule(fid, LikesModuleEnum.BLOG.getValue());
            userLikesCount += likesCount;

            int collectCount = collectService.selectByFidAndModule(fid, LikesModuleEnum.BLOG.getValue());
            userCollectCount += collectCount;  // 用户收到的累加收藏数量
        }
        user.setLikesCount(userLikesCount);
        user.setCollectCount(userCollectCount);


        blog.setUser(user);  // 设置作者信息
        // 查询当前博客的点赞数据
        int likesCount = likesService.selectByFidAndModule(id, LikesModuleEnum.BLOG.getValue());
        blog.setLikesCount(likesCount);
        Likes userLikes = likesService.selectUserLikes(id, LikesModuleEnum.BLOG.getValue());
        blog.setUserLike(userLikes != null);

        // 查询当前博客的收藏数据
        int collectCount = collectService.selectByFidAndModule(id, LikesModuleEnum.BLOG.getValue());
        blog.setCollectCount(collectCount);
        Collect userCollect = collectService.selectUserCollect(id, LikesModuleEnum.BLOG.getValue());
        blog.setUserCollect(userCollect != null);
        return blog;
    }

    /**
     * 查询所有
     * @param blog
     * @return
     */
    public List<Blog> selectAll(Blog blog) {
        return blogMapper.selectAll(blog);
    }

    /**
     * 分页查询
     * @param blog
     * @param pageNum
     * @param pageSize
     * @return
     */
    public PageInfo<Blog> selectPage(Blog blog, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Blog> list = blogMapper.selectAll(blog);
        for (Blog blog1 : list) {
            int likesCount=likesService.selectByFidAndModule(blog1.getId(),LikesModuleEnum.BLOG.getValue());
            blog1.setLikesCount(likesCount);
        }
        return PageInfo.of(list);
    }

    /**
     * 置顶/取消置顶（仅管理员可调用，调用方需校验角色）
     * @param id   博客ID
     * @param top  1置顶 0取消
     */
    public void setTop(Integer id, Integer top) {
        blogMapper.setTop(id, top);
    }

    /**
     * 博客榜单
     * @return
     */
    public List<Blog> selectTop() {
        List<Blog> blogList = this.selectAll(null);
        blogList= blogList.stream().sorted((b1, b2) -> b2.getReadCount().compareTo(b1.getReadCount()))
                .limit(20)
                .collect(Collectors.toList());
        return blogList;
    }

    /**
     * 博客推荐
     * @param blogId
     * @return
     */
    public Set<Blog> selectRecommend(Integer blogId) {
        Blog blog = this.selectById(blogId);
        String tags = blog.getTags();
        Set<Blog> blogSet=new HashSet<>();
        if (ObjUtil.isNotEmpty(tags)){
            List<Blog> blogList = this.selectAll(null);
            JSONArray tagsArr = JSONUtil.parseArray(tags);
            for (Object tag : tagsArr) {
                //筛选出包含当前博客标签的其他的博客列表
                Set<Blog> collect=blogList.stream().filter(b->b.getTags().contains(tag.toString())&& !blogId.equals(b.getId()))
                        .collect(Collectors.toSet());
                blogSet.addAll(collect);
            }
        }
        blogSet=blogSet.stream().limit(5).collect(Collectors.toSet());
        blogSet.forEach(b->{
            int likesCount=likesService.selectByFidAndModule(b.getId(),LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likesCount);
        });
        return blogSet;
    }

    /**
     * 更新阅读量
     * @param blogId
     */
    public void updateReadCount(Integer blogId) {
        blogMapper.updateReadCount(blogId);
    }

    /**
     * 分页查询 用户发表过的博客
     * @param blog
     * @param pageNum
     * @param pageSize
     * @return
     */
    public PageInfo<Blog> selectUserBlog(Blog blog, Integer pageNum, Integer pageSize) {
        Account currentUser = TokenUtils.getCurrentUser();
        if(RoleEnum.USER.name().equals(currentUser.getRole())){
            blog.setUserId(currentUser.getId());
        }
        return this.selectPage(blog,pageNum,pageSize);
    }

    /**
     * 分页查询 用户点赞的博客
     * @param blog
     * @param pageNum
     * @param pageSize
     * @return
     */
    public PageInfo<Blog> selectUserLike(Blog blog, Integer pageNum, Integer pageSize) {
        Account currentUser = TokenUtils.getCurrentUser();
        if(RoleEnum.USER.name().equals(currentUser.getRole())){
            blog.setUserId(currentUser.getId());
        }
        PageHelper.startPage(pageNum,pageSize);
        List<Blog> list = blogMapper.selectUserLike(blog);
        PageInfo<Blog> pageInfo = PageInfo.of(list);
        List<Blog> blogList = pageInfo.getList();
        for (Blog b : blogList){
            int likeCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likeCount);
        }
        return pageInfo;
    }

    /**
     * 分页查询 用户收藏的博客
     * @param blog
     * @param pageNum
     * @param pageSize
     * @return
     */
    public PageInfo<Blog> selectUserCollect(Blog blog, Integer pageNum, Integer pageSize) {
        Account currentUser = TokenUtils.getCurrentUser();
        if(RoleEnum.USER.name().equals(currentUser.getRole())){
            blog.setUserId(currentUser.getId());
        }
        PageHelper.startPage(pageNum,pageSize);
        List<Blog> list = blogMapper.selectUserCollect(blog);
        PageInfo<Blog> pageInfo = PageInfo.of(list);
        List<Blog> blogList = pageInfo.getList();
        for (Blog b : blogList){
            int likeCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likeCount);
        }
        return pageInfo;
    }

    /**
     * 分页查询 用户评论的博客
     * @param blog
     * @param pageNum
     * @param pageSize
     * @return
     */
    public PageInfo<Blog> selectUserComment(Blog blog, Integer pageNum, Integer pageSize) {
        Account currentUser = TokenUtils.getCurrentUser();
        if(RoleEnum.USER.name().equals(currentUser.getRole())){
            blog.setUserId(currentUser.getId());
        }
        PageHelper.startPage(pageNum,pageSize);
        List<Blog> list = blogMapper.selectUserComment(blog);
        PageInfo<Blog> pageInfo = PageInfo.of(list);
        List<Blog> blogList = pageInfo.getList();
        for (Blog b : blogList){
            int likeCount = likesService.selectByFidAndModule(b.getId(), LikesModuleEnum.BLOG.getValue());
            b.setLikesCount(likeCount);
        }
        return pageInfo;
    }
}