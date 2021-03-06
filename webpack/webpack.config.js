var ExtractTextPlugin = require('extract-text-webpack-plugin');
module.exports = {
  entry: './app/newsticker.js',
  output: {
    filename: 'newsticker.js',
    path: '../src/collective/newsticker/browser/static',
    libraryTarget: 'umd',
    publicPath: '/++resource++collective.newsticker/',
    library: 'collective.newsticker'
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /\.less$/,
      exclude: /node_modules/,
      loader: ExtractTextPlugin.extract({
        fallbackLoader: 'style-loader',
        loader: 'css-loader?importLoaders=1!postcss-loader!less-loader'
      })
    }, {
      test: /.*\.(gif|png|jpe?g)$/i,
      loaders: [
        'file-loader?name=[path][name].[ext]&context=app/',
        {
          loader: 'image-webpack-loader',
          query: {
            progressive: true,
            pngquant: {
              quality: '65-90',
              speed: 4
            },
            gifsicle: {
              interlaced: false
            },
            optipng: {
              optimizationLevel: 7
            }
          }
        }
      ]
    }, {
      test: /\.svg/,
      exclude: /node_modules/,
      use: 'svg-url-loader'
    }]
  },
  devtool: 'source-map',
  plugins: [
    new ExtractTextPlugin({ filename: 'newsticker.css', disable: false, allChunks: true })
  ]
}
