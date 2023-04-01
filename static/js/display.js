  //   vueApp = new Vue({
  //       el: "#contentdisplay",
  //       delimiters: ["[[", "]]"],
  //       data() {
  //           return {
  //               detail: {},
  //           };
  //       },
  // methods: {
  //   currentDate() {
  //     const current = new Date();
  //     return `${current.getHours()}:${current.getMinutes() + 1}/${current.getSeconds()}`;
  //   }
  // }
  //   });
  //
  //
  //   const ws = new WebSocket("ws://localhost:8000/view/data/")
  //   ws.setReadTimeout = 30000;
  //   if (ws.readyState === WebSocket.OPEN) {
  //       console.log('WebSocket open...');
  // // Connection is open, read messages
  //   } else if (ws.readyState === WebSocket.CLOSED) {
  //     console.error('WebSocket connection closed');
  //   } else if (ws.readyState === WebSocket.CONNECTING) {
  //     console.log('WebSocket connecting...');
  //   } else if (ws.readyState === WebSocket.CLOSING) {
  //     console.log('WebSocket closing...');
  //   } else {
  //     console.error('Unknown WebSocket state:', ws.readyState);
  //   }
  //
  //   ws.onopen = function () {
  //       ws.send(JSON.stringify({
  //           action: "retrieve",
  //           request_id: new Date().getTime(),
  //       }))
  //   }
  //   ws.onmessage = function (e) {
  //       setTimeout(() => {
  //           const allData = JSON.parse(e.data);
  //           console.log(allData);
  //       if (allData.action === "retrieve") {
  //           vueApp.$data.detail = allData.data;
  //           vueApp.$forceUpdate();
  //           $("#contentdisplay").css("display","none");
  //       }else if (allData.action === "create") {
  //         vueApp.$data.detail = allData.data;
  //         vueApp.$forceUpdate();
  //          setInterval(function(){
  //               $("#contentdisplay").fadeOut("slow");
  //           }, 5000);
  //          $("#contentdisplay").css("display","block");
  //       }
  // }, 5000);
  //   }

      vueApp = new Vue({
        el: "#contentdisplay",
        delimiters: ["[[", "]]"],
        data() {
            return {
                detail: {},
            };
        },
      methods: {
        currentDate() {
        const current = new Date();
        return `${current.getHours()}:${current.getMinutes() + 1}:${current.getSeconds()}`;
    }
  }
    });

    const ws = new WebSocket("ws://localhost:8000/view/data/")
    let currentData = '';

    ws.onopen = function () {
        ws.send(JSON.stringify({
            action: "retrieve",
            request_id: new Date().getTime(),
        }))
    }
    ws.onmessage = function (e) {
        const allData = JSON.parse(e.data);
        if (allData !== currentData) {
            // Update current message
            currentData = allData;
            // Take any necessary actions based on the difference
            console.log('New message received:', currentMessage);
          }
        if (allData.action === "retrieve") {
            vueApp.$data.detail = allData.data;
            vueApp.$forceUpdate();
            $("#contentdisplay").css("display","none");
        }else if (allData.action === "create") {
            vueApp.$data.detail = allData.data;
            vueApp.$forceUpdate();
            $("#contentdisplay").css("display","block");
            $("#contentdisplay").fadeOut(7000);
            console.log("Current data: "+currentData);
            console.log("previous data: "+previous);



        }
    }
