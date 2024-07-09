import request from '@/utils/request'
const MENU_BASE_URL = '/api/menu'

class MenuAPI {
    /**
    * 获取当前用户的路由列表
    * <p/>
    * 无需传入角色，后端解析token获取角色自行判断是否拥有路由的权限
    *
    * @returns 路由列表
    */
    static getRoutes() {
        return request<any,RouteView[]>({
            url: `${MENU_BASE_URL}/routes`,
            method: 'get'
        });
    }

    /**
     * 获取菜单列表
     * @returns 菜单列表
     */
    static getOptions() {
        return request<any,OptionType[]>({
            url: `${MENU_BASE_URL}/options`,
            method: 'get'
        });
    }

    /**
     * 获取菜单表单数据
     * @param id 菜单ID
     * @returns 菜单表单数据
     */
    static getFormData(id: number) {
        return request<any,MenuForm>({
            url: `${MENU_BASE_URL}/${id}/form`,
            method: 'get'
        });
    }

    /**
     * 新增菜单
     * @param data 菜单数据
     * @returns 结果
     */
    static add(data: MenuForm) {
        return request({
            url: `${MENU_BASE_URL}`,
            method: 'post',
            data
        });
    }
    
    /**
     * 修改菜单
     * @param id 菜单ID
     * @param data 菜单数据
     * @returns 结果
     */
    static update(id: number, data: MenuForm) {
        return request({
            url: `${MENU_BASE_URL}/${id}`,
            method: 'put',
            data: data,
        });
    }

    /**
     * 删除菜单
     * @param id 菜单ID
     * @returns 结果
     */
    static delete(id: number) {
        return request({
            url: `${MENU_BASE_URL}/${id}`,
            method: 'delete'
        });
    }
}

export default MenuAPI;

import { MenuTypeEnum } from '@/enums/menuTypeEnum';

/** 菜单查询参数 */
export interface MenuQuery {
    /** 搜索关键字 */
    keywords?:string;
}

/** 菜单视图对象 */
export interface MenuView {
    /** 子菜单 */
    children?: MenuView[];
    /** 组件路径 */
    component?: string;
    /** ICON */
    icon?: string;
    /** 菜单ID */
    id?: number;
    /** 菜单名称 */
    name?: string;
    /** 父菜单ID */
    parentId?: number;
    /** 按钮权限标识 */
    perm?: string;
    /** 跳转路径 */
    redirect?: string;
    /** 路由名称 */
    routeName?: string;
    /** 路由相对路径 */
    routePath?: string;
    /** 菜单排序(数字越小排名越靠前) */
    sort?: number;
    /** 菜单 */
    type?: MenuTypeEnum;
    /** 菜单是否可见(1:显示;0:隐藏) */
    visible?: number;
}

/** 菜单表单对象 */
export interface MenuForm {
    /** 菜单ID */
    id?: string;
    /** 父菜单ID */
    parentId?: number;
    /** 菜单名称 */
    name?: string;
    /** 菜单是否可见(1-是 0-否) */
    visible: number;
    /** ICON */
    icon?: string;
    /** 排序 */
    sort?: number;
    /** 路由名称 */
    routeName?: string;
    /** 路由路径 */
    routePath?: string;
    /** 组件路径 */
    component?: string;
    /** 跳转路由路径 */
    redirect?: string;
    /** 菜单 */
    type?: MenuTypeEnum;
    /** 权限标识 */
    perm?: string;
    /** 【菜单】是否开启页面缓存 */
    keepAlive?: number;
    /** 【目录】只有一个子路由是否始终显示 */
    alwaysShow?: number;
    /** 参数 */
    params?: KeyValue[];
}

interface KeyValue {
    key: string;
    value: string;
}

/** RouteView，路由对象 */
export interface RouteView {
    /** 子路由列表 */
    children: RouteView[];
    /** 组件路径 */
    component?: string;
    /** 路由属性 */
    meta?: Meta;
    /** 路由名称 */
    name?: string;
    /** 路由路径 */
    path?: string;
    /** 跳转链接 */
    redirect?: string;
}

/** Meta，路由属性 */
export interface Meta {
    /** 【目录】只有一个子路由是否始终显示 */
    alwaysShow?: boolean;
    /** 是否隐藏(true-是 false-否) */
    hidden?: boolean;
    /** ICON */
    icon?: string;
    /** 【菜单】是否开启页面缓存 */
    keepAlive?: boolean;
    /** 路由title */
    title?: string;
}
