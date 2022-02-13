const { VueLoaderPlugin } = require('vue-loader');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const path = require('path');

module.exports = {
  entry: {
    login: './assets/login.js',
    home: './assets/home.js',
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname) + '/dist/js/',
  },
  module: {
    rules: [
      // JavaScript: Use Babel to transpile JavaScript files
      { test: /\.vue$/, loader: 'vue-loader' },
      { test: /\.js$/, exclude: /node_modules/, use: ['babel-loader'] },
    ],
  },
  plugins: [new VueLoaderPlugin(), new CleanWebpackPlugin({ verbose: true })],
};
