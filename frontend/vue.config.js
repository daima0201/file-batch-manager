const path = require('path');

module.exports = {
    // 打包后的静态资源输出目录 backend/statics
    outputDir: path.resolve(__dirname, '../backend/static'), // index.html 输出到 backend/templates
    indexPath: path.resolve(__dirname, '../templates/index.html'),

    // 生产环境构建时禁用 source map（可选）
    productionSourceMap: false,

    // 开发服务器配置
    devServer: {
        host: 'localhost', port: 8080, open: true, // 自动打开浏览器
        proxy: {
            '/api': {
                target: 'http://localhost:8000', // Django 开发服务地址
                changeOrigin: true
            }
        }, historyApiFallback: {
            index: '/index.html' // 支持 history 模式路由
        }
    },

    // 修改静态资源路径（可选，Django 可以通过 STATICFILES_DIRS 找到）
    assetsDir: 'assets',

    // 输出文件名 hash（可选）
    filenameHashing: true,

    // Webpack 自定义配置（可选扩展）
    configureWebpack: {
        resolve: {
            alias: {
                '@': path.resolve(__dirname, 'src') // 可用 @ 引用 src 目录
            }
        }
    }
};