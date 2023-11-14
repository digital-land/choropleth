module.exports = {
  multipass: true,
  js2svg: {
    indent: 2,
    pretty: true,
  },
  plugins: [
     {
      name: 'preset-default',
      params: {
        overrides: {
          cleanupIds: false,
        },
      },
    },
    {
      name: "removeAttrs",
      params: {
        attrs: "(style)"
      }
    },
    {
      name: "removeDimensions"
    },
  ],
};
