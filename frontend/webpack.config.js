/* eslint-disable @typescript-eslint/no-var-requires */
const path = require('path')
const BundleTracker = require('webpack4-bundle-tracker')
const { CheckerPlugin } = require('awesome-typescript-loader')

module.exports = {
  mode: 'production',
  entry: [
    './src/index.tsx',
  ],
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
