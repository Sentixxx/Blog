<template>
    <div class="s-canvas" @click="refreshCode">
        <canvas id="s-canvas" :width="contentWidth" :height="contentHeight"></canvas>
    </div>
</template>
<script setup lang="ts">
let curCaptchaCode = ref('')

const props = defineProps({
    captchaCode: {
        type: String,
        default: '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    },
    fontSizeMin: {
        type: Number,
        default: 16
    },
    fontSizeMax: {
        type: Number,
        default: 40
    },
    backgroundColorMin: {
        type: Number,
        default: 180
    },
    backgroundColorMax: {
        type: Number,
        default: 240
    },
    colorMin: {
        type: Number,
        default: 50
    },
    colorMax: {
        type: Number,
        default: 160
    },
    lineColorMin: {
        type: Number,
        default: 40
    },
    lineColorMax: {
        type: Number,
        default: 180
    },
    dotColorMin: {
        type: Number,
        default: 0
    },
    dotColorMax: {
        type: Number,
        default: 255
    },
    contentWidth: {
        type: Number,
        default: 112
    },
    contentHeight: {
        type: Number,
        default: 38
    }
})

watch(curCaptchaCode, () => {
    drawPic()
})

const emit = defineEmits(['updateCaptchaCode'])

// 生成一个随机数
const randomNum = (min: number, max: number) => {
    return Math.floor(Math.random() * (max - min) + min)
}
// 生成一个随机的颜色
const randomColor = (min: number, max: number) => {
    let r = randomNum(min, max)
    let g = randomNum(min, max)
    let b = randomNum(min, max)
    return 'rgb(' + r + ',' + g + ',' + b + ')'
}
const drawPic = () => {
    const canvas = document.getElementById('s-canvas') as HTMLCanvasElement
    if (canvas === null) {
        console.error('unable to get canvas')
        return
    }
    const ctx = canvas.getContext('2d')
    if (ctx) {
        ctx.textBaseline = 'bottom'
        ctx.fillStyle = randomColor(props.backgroundColorMin, props.backgroundColorMax) // 随机颜色
        ctx.fillRect(0, 0, props.contentWidth, props.contentHeight)
        for (let i = 0; i < curCaptchaCode.value.length; i++) {
            drawText(ctx, curCaptchaCode.value[i], i)
        }
        drawLine(ctx) // 绘制干扰线
        drawDot(ctx) // 绘制干扰点
    } else {
        console.error('unable to get 2d context')
    }
}
const drawText = (ctx: CanvasRenderingContext2D, txt: string, i: number) => {
    ctx.fillStyle = randomColor(props.colorMin, props.colorMax)
    ctx.font = randomNum(props.fontSizeMin, props.fontSizeMax) + 'px SimHei'
    let x = (i + 1) * (props.contentWidth / (curCaptchaCode.value.length + 1))
    let y = randomNum(props.fontSizeMax, props.contentHeight - 3)
    let deg = randomNum(-30, 30)
    // 修改坐标原点和旋转角度
    ctx.translate(x, y)
    ctx.rotate((deg * Math.PI) / 180)
    ctx.fillText(txt, 0, 0)
    // 恢复坐标原点和旋转角度
    ctx.rotate((-deg * Math.PI) / 180)
    ctx.translate(-x, -y)
}
const drawLine = (ctx: CanvasRenderingContext2D) => {
    // 绘制干扰线
    for (let i = 0; i < 2; i++) {
        ctx.strokeStyle = randomColor(props.lineColorMin, props.lineColorMax)
        ctx.beginPath()
        ctx.moveTo(randomNum(0, props.contentWidth), randomNum(0, props.contentHeight))
        ctx.lineTo(randomNum(0, props.contentWidth), randomNum(0, props.contentHeight))
        ctx.stroke()
    }
}
const drawDot = (ctx: CanvasRenderingContext2D) => {
    // 绘制干扰点
    for (let i = 0; i < 30; i++) {
        ctx.fillStyle = randomColor(0, 255)
        ctx.beginPath()
        ctx.arc(
            randomNum(0, props.contentWidth),
            randomNum(0, props.contentHeight),
            1,
            0,
            2 * Math.PI
        )
        ctx.fill()
    }
}

const refreshCode = () => {
    // console.log('refreshCode')
    curCaptchaCode.value = ''
    makeCode(props.captchaCode, 4)
}
const makeCode = (origin: string, len: number) => {
    for (let i = 0; i < len; i++) {
        curCaptchaCode.value += origin[randomNum(0, origin.length)]
    }
    emit('updateCaptchaCode', curCaptchaCode.value)
}

onMounted(() => {
    drawPic()
    refreshCode()
})

defineExpose({
    refreshCode
})
</script>
