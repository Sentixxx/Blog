/* 消息类型枚举 */
export const enum MessageTypeEnum {
    /* 消息 */
    MESSAGE = 'MESSAGE',
    /* 通知 */
    NOTICE = 'NOTICE',
    /* 待办 */
    WARNING = 'WARNING',
}

export const MessageTypeLabels = {
    [MessageTypeEnum.MESSAGE]: '消息',
    [MessageTypeEnum.NOTICE]: '通知',
    [MessageTypeEnum.WARNING]: '警告'
}
