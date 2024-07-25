<template>
    <div>
        <el-collapse v-model="showSearch" accordion>
            <el-collapse-item name="1">
                <template slot="title">
                    <i class="header-icon el-icon-search"> 搜索条件，点击显示/隐藏</i>
                </template>
                <div class="search">
                    <template v-for="(item, index) in model">
                        <el-input
                            v-if="item.control == 'text'"
                            class="input"
                            v-model="item.value"
                            size="mini"
                            clearable
                            :key="index"
                        >
                        <template slot="prepend">{{ item.label }}:</template>
                        </el-input>
                        <div v-else-if="item.control == 'dropdown'" :key="index" class="dropdown">
                            <span class="span">{{ item.label }}:</span>
                            <el-select v-model="item.value" size="mini" clearable>
                                <el-option
                                    v-for="dItem in getdict(item.dictType - 1, item.custom)"
                                    :key="dItem.value"
                                    :label="dItem.name"
                                    :value="dItem.value"
                                />
                            </el-select>
                        </div>
                        <div v-else-if="item.control == 'age'" class="age" :key="index">
                            <span class="span">{{ item.label }}:</span>
                            <div class="ageSlider">
                                <el-slider v-model="item.value" range :max="150"> </el-slider>
                            </div>
                        </div>
                        <div v-else-if="item.control == 'dateRange'" class="dateRange" :key="index">
                            <span class="span">{{ item.label }}:</span>
                            <el-date-picker
                                clearable
                                v-model="item.value"
                                type="daterange"
                                align="center"
                                size="small"
                                unlink-panels
                                range-separator="—-"
                                start-placeholder="开始日期"
                                end-placeholder="结束日期"
                                value-format="yyyy-MM-dd"
                                :picker-options="pickerOptions"
                            >
                            </el-date-picker>
                        </div>
                    </template>

                    <slot>buttons area</slot>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
export default {
    name: 'WSearch',
    props: {
        model: {
            type: Array,
            default: () => {
                return []
            }
        },
        dict: { type: Array, default: () => [] },
        show: { type: String, default: '' }
    },
    created() {},
    data() {
        return {
            marks: {
                50: '50岁',
                100: '100岁'
            },
            pickerOptions: {
                shortcuts: [
                    {
                        text: '今天',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            picker.$emit('pick', [start, end])
                        }
                    },
                    {
                        text: '昨天',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            start.setTime(start.getTime() - 3600 * 1000 * 24)
                            picker.$emit('pick', [start, end])
                        }
                    },
                    {
                        text: '最近一周',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
                            picker.$emit('pick', [start, end])
                        }
                    },
                    {
                        text: '最近一个月',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
                            picker.$emit('pick', [start, end])
                        }
                    },
                    {
                        text: '最近三个月',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
                            picker.$emit('pick', [start, end])
                        }
                    }
                ]
            },
            listQuery: {
                page: 1,
                limit: 10,
                account: undefined,
                name: undefined
            },
            customDict: [],
            showSearch: this.show
        }
    },
    methods: {
        handleInput(e, index) {
            //this.$emit("input", this.model);
        },
        getCustomDict(url) {
            return this.$http.fetch({
                url: url,
                method: 'get'
            })
        },
        getdict(index, url) {
            if (url) {
                return this.customDict[url] || []
            } else if (this.dict && this.dict.length > index) {
                var d = [
                    {
                        name: '全选',
                        value: ''
                    },
                    ...this.dict[index]
                ]
                return d
            } else {
                //console.log('dict',this.dict)
                return []
            }
        }
    }
}
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
.search {
    display: flex;
    display: -webkit-flex; /* Safari */
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: left;
    align-items: center;
    .span {
        border-left: 1px solid #dcdfe6;
        border-top: 1px solid #dcdfe6;
        border-bottom: 1px solid #dcdfe6;
        border-right: 0;
        border-top-left-radius: 4px;
        border-bottom-left-radius: 4px;
        //width:60px;
        background-color: #f5f7fa;
        color: #909399;
        vertical-align: middle;
        display: table-cell;
        position: relative;
        margin-right: 0px;
        padding: 0 20px;
        white-space: nowrap;
        height: 28px;
    }
    .input {
        width: 240px;
        margin: 5px;
    }
    .dropdown {
        width: 240px;
        margin: 5px;
        display: flex;
        display: -webkit-flex; /* Safari */
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: center;

        ::v-deep input {
            border-top-left-radius: 0;
            border-bottom-left-radius: 0;
            width: 100%;
            min-width: 150px;
        }
    }
    .age {
        width: 240px;
        margin: 5px;
        display: flex;
        display: -webkit-flex; /* Safari */
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: center;
        .ageSlider {
            width: 100%;
            min-width: 150px;
            border: 1px solid #dcdfe6;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            height: 28px;
            align-self: flex-start;
            padding: 0 10px 0 10px;
        }
        ::v-deep .el-slider__bar {
            background-color: #aaa;
        }
    }
    .dateRange {
        min-width: 250px;
        margin: 5px;
        display: flex;
        display: -webkit-flex; /* Safari */
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: left;
        align-items: center;
        flex-grow: 1;
        ::v-deep .el-input__inner {
            border-top-left-radius: 0;
            border-bottom-left-radius: 0;
        }
        .span {
            height: 32px;
        }
        ::v-deep input {
            width: 100%;
            min-width: 80px;
        }
    }
}
</style>
