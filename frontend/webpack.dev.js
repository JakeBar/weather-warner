/* eslint-disable @typescript-eslint/no-var-requires */
const path = require('path')
const merge = require('webpack-merge')
const webpack = require('webpack')
const base = require('./webpack.config.js')

module.exports = merge(base, {
  mode: 'development',
  entry: [
    'react-hot-loader/patch',
  ],
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
  ],
  devServer: {
    // Where the webpack dev server serve the static files, should be the same as output.path
    contentBase: path.resolve(__dirname, '../static/build'),
    // Enable hot reload
    hot: true,
    // Port number for webpack dev server
    port: 9009,
    host: 'localhost',
    // Enable Django to serve this cross origin
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    // The public URL of the output resource directory (CDN), should be the same as output.publicPath
    publicPath: 'https://localhost:9009/static/build/',
    https: true,
    disableHostCheck: true,
  },
  output: {
    filename: '[name].[hash].js',
    publicPath: 'https://localhost:9009/static/build/',
  },
})
