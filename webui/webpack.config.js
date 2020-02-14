const path = require('path');
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { getIfUtils, removeEmpty } = require('webpack-config-utils');
const autoprefixer = require('autoprefixer');

const APP_NAME = process.env.ENV_APP_NAME || 'app';
console.log('webpack: APP_NAME is ' + APP_NAME);

const PUBLIC_PATH = process.env.ENV_PUBLIC_PATH || '';
console.log('webpack: PUBLIC_PATH is ' + PUBLIC_PATH);

const NODE_ENV = process.env.NODE_ENV || 'development';
const { ifProduction, ifDevelopment } = getIfUtils(NODE_ENV);

const definePluginVars = {
  'process.env.APP_NAME': JSON.stringify(APP_NAME),
  'process.env.NODE_ENV': JSON.stringify(NODE_ENV),
  'process.env.DEVELOPMENT': JSON.stringify(ifDevelopment(true, false)),
};

const getAppEntry = () => {
  return {
    app: removeEmpty([
      '@babel/polyfill',
      ifDevelopment('webpack-hot-middleware/client'),
      './src/index.js',
    ]),
  };
};

const getLessLoaders = useModules => {
  return [
    ifProduction(
      { loader: MiniCssExtractPlugin.loader },
      {
        loader: 'style-loader', // creates style nodes from JS strings
        options: {},
      }
    ),
    {
      loader: 'css-loader', // translates CSS into CommonJS
      options: useModules
        ? {
            modules: {
              localIdentName: '[name]__[local]--[hash:base64:5]',
            },
          }
        : {},
    },
    {
      loader: 'postcss-loader',
      options: {
        plugins: () => [autoprefixer],
      },
    },
    {
      loader: 'less-loader', // compiles Less to CSS
      options: {
        // modifyVars: {
        //   'primary-color': '#1DA57A',
        //   'link-color': '#1DA57A',
        //   'border-radius-base': '2px'
        // },
        javascriptEnabled: true,
      },
    },
  ];
};

module.exports = {
  mode: NODE_ENV,
  entry: getAppEntry(),
  output: {
    path: path.resolve(__dirname, `build/dist`),
    publicPath: PUBLIC_PATH,
    filename: ifProduction('app-[hash].js', 'app.js'),
    chunkFilename: ifProduction('[id].bundle-[chunkhash].js', '[id].bundle.js'),
  },

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx'],
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            cacheDirectory: './build/babel_cache',
          },
        },
      },

      // CSS
      {
        test: /\.css$/,
        use: [ifProduction(MiniCssExtractPlugin.loader, 'style-loader'), 'css-loader'],
      },

      // LESS
      { test: /\.less$/, include: [path.resolve(__dirname, 'src')], use: getLessLoaders(true) },
      { test: /\.less$/, exclude: [path.resolve(__dirname, 'src')], use: getLessLoaders(false) },

      // images
      {
        test: /\.(png|jpg|gif)$/,
        use: [
          {
            loader: 'file-loader',
            options: {},
          },
        ],
      },
      {
        test: /\.svg$/,
        use: ['@svgr/webpack', 'url-loader'],
      },
    ],
  },

  plugins: removeEmpty([
    ifProduction(new CleanWebpackPlugin()),
    ifProduction(
      new MiniCssExtractPlugin({
        filename: 'app-[hash].css',
        chunkFilename: 'app.[id]-[hash].css',
      })
    ),
    ifDevelopment(new webpack.HotModuleReplacementPlugin()),
    new webpack.DefinePlugin(definePluginVars),
    new HtmlWebpackPlugin({
      template: './src/index.html',
      filename: './index.html',
      minify: false,
      hash: false,
    }),
    ifProduction(
      new CopyWebpackPlugin([
        {
          context: 'assets',
          from: { glob: '**/*' },
          to: '.',
        },
      ])
    ),
  ]),

  devtool: ifDevelopment('source-map'),

  optimization: {
    splitChunks: {
      chunks: 'all',
    },
  },
};
