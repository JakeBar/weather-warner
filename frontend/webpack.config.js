/* eslint-disable @typescript-eslint/no-var-requires */
const path = require('path')
const BundleTracker = require('webpack4-bundle-tracker')
const { CheckerPlugin } = require('awesome-typescript-loader')

const context = path.resolve(__dirname, 'src')
module.exports = {
  mode: 'production',
  context,
  entry: './index.tsx',
  devtool: 'inline-source-map',
  plugins: [
    new BundleTracker({ filename: './webpack-stats.json' }),
    new CheckerPlugin(),
  ],
  output: {
    path: path.resolve(__dirname, '../static/build'),
    filename: '[name].[chunkhash].js',
    publicPath: '/static/build/',
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'awesome-typescript-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: [ '.tsx', '.ts', '.jsx', '.js','.html' ],
  },
}
