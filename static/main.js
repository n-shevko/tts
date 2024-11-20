Vue.createApp({
  data() {
    return Object.assign({
          inProgress: false,
          textareaValue: '',
          selectedFile: null
        },
        window.vueData
      )
  },
  watch: {
    'model': {
        handler(newValue, oldValue) {
          let self = this;
          this.inProgress = true;
          fetch('/switch_model', {
            method: 'POST',
            body: JSON.stringify({model: newValue}),
            headers: {
              'Content-Type': 'application/json',
            }
          }).then(response => response.json())
            .then(data => {
              self.speakers = data.speakers;
              self.speaker = data.speaker;
              self.inProgress = false;
            })
        }
    }
  },
  computed: {
    speedRounded() {
      return parseFloat(this.speed).toFixed(2);
    }
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    saveParams() {
      let params = {};
      ['source', 'model', 'speaker', 'speed'].forEach(key => {
        params[key] = this[key];
      })
      fetch('/save_params', {
        method: 'POST',
        body: JSON.stringify(params),
        headers: {
          'Content-Type': 'application/json',
        }
      })
    },
    filename() {
      const now = new Date();
      const year = now.getFullYear();
      const day = String(now.getDate()).padStart(2, '0');
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const seconds = String(now.getSeconds()).padStart(2, '0');
      return `${day}_${month}_${year}_${hours}_${minutes}_${seconds}`;
    },
    createMp3() {
      let self = this;
      this.inProgress = true;

      const formData = new FormData();
      if (this.source === 'file') {
        formData.append('file', this.selectedFile);
      } else {
        formData.append('text', this.textareaValue);
      }
      fetch('/create_mp3', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.blob())
        .then(blob => {
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = this.filename() + '.mp3';
          document.body.appendChild(a);
          a.click();
          a.remove();
          URL.revokeObjectURL(url);
        })
        .finally(() => {
          self.inProgress = false;
        });
    }
  }
}).mount('#app')