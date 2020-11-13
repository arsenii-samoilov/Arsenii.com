const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: {
    main: ['./src/js/main.ts', './src/css/style.css'],
  },
  output: {
    filename: 'js/main-[contenthash:12].js',
    path: path.resolve(__dirname, 'dist'),
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: path.resolve(__dirname, 'dist/index.ejs'),
      template: '!!raw-loader!src/views/index.ejs',
      minify: false,
    }),
    new MiniCssExtractPlugin({
      filename: 'css/style-[contenthash:12].css',
    }),
    new CopyPlugin({
      patterns: [
        { from: 'src/views/error.ejs', to: path.resolve(__dirname, 'dist') },
      ],
    }),
  ],
};
