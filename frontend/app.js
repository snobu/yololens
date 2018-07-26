let PacmanLoader = VueSpinner.PacmanLoader;
let postUrl = '/api/images';

Vue.component("child", {
  props: {
    noResponse: { type: Boolean }
  },
  data: function data() {
    return {
      renderCache: undefined
    };
  },

  methods: {
    // methods
  },
  template: "#child"
});

new Vue({
  el: "#app",
  components: {
    PacmanLoader
  },
  data: function data() {
    return {
      spinnerColor: '#fff',
      thing: {},
      predictions: {},
      image: "",
      noResponse: false,
      apiError: {}
    };
  },

  methods: {
    detect: function detect() {
      var _this = this;

      var data = void 0,
          contentType = void 0;
      if (typeof this.image === "string") {
        data = { url: this.image };
        contentType = "application/json";
      } else {
        data = this.image;
        console.log(`POSTing as ${this.type}`);
        contentType = this.type;
      }
      
      axios({
        method: "post",
        url: postUrl,
        data: data,
        timeout: 180000,
        headers: {
          "Content-Type": contentType
        }
      }).then(function (response) {
        if (response.status == 200 | response.status == 201 | response.status == 202) {
          _this.thing = { img: response.headers.location };
          _this.predictions = response.data;
        }
        else {
          console.error('Something has gone awfully bad.');
          console.log('response.headers.location = ', response.headers.location);
          console.log('response.status = ', response.status, response.statusText);
        }
      }).catch(function (error) {
        if (error.response) {
          _this.apiError.status = error.response.status
          _this.apiError.statusText = error.response.statusText
          _this.apiError.message = error.response.message
        }
      });
    },
    
    fileUpload: function fileUpload(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      this.image = files[0];
      this.type = files[0].type;
      console.log(`MIME type: ${this.type}`);
      this.createImage();
      this.detect();
    },
  
    useMine: function useMine() {
      this.image = 'https://yolovision.blob.core.windows.net/samples/roads-india.jpg';
      this.detect();
    },

    createImage: function createImage() {
      var _this2 = this;

      var image = new Image();
      var reader = new FileReader();

      reader.onload = function (e) {
        _this2.image = e.target.result;
      };
      reader.readAsDataURL(this.image);
    },

    removeImage: function removeImage(e) {
      this.image = "";
      this.noResponse = false;
      this.thing = {};
      this.predictions = {};
      this.apiError = {};
    }
  }
});
