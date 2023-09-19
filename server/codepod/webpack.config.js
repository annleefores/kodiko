const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    target: 'node',
    entry: './src/server.ts',
    output: {
        filename: 'server.js',
        path: path.resolve(__dirname, 'dist'),
    },
    externals: {
        'node-pty': 'commonjs node-pty'
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },

        ],
    },
    ignoreWarnings: [
        {
            module: /\.\/node_modules\/express\/lib\/view\.js\?[34]/, // A RegExp
        },
        {
            message: /the warning/,
        },

        (warning) => true,
    ],

    resolve: {
        extensions: ['.tsx', '.ts', '.js'],

    },
    devtool: 'source-map',
    plugins: [
        new CopyWebpackPlugin({
            patterns: [
                { from: 'node_modules/node-pty/', to: 'node_modules/node-pty/' },
            ],
        }),
    ],
};