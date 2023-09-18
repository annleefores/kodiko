const path = require('path');

module.exports = {
    target: 'node',
    entry: './src/server.ts',
    output: {
        filename: 'server.js',
        path: path.resolve(__dirname, 'dist'),
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
};