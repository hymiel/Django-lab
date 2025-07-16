const callGet = (url) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: 'get',
            contentType: 'application/json',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                resolve(response);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
};


const callPost = (body, url) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(body),
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            crossDomain: true,
            success: function (response) {
                resolve(response);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
};


const callDelete = (body, url) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: 'delete',
            contentType: 'application/json',
            data: JSON.stringify(body),
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                resolve(response);
            },
            error: function (error) {
                reject(error);
            }
        })
    })
};




const callAPI = (method, path, data) => {
    // const fullUrl = `${BASE_URL}${path}`;
    const fullUrl = path;

    return new Promise((resolve, reject) => {
      $.ajax({
        url: fullUrl,
        type: method,
        beforeSend: function (xhr, opts) {
          if (localStorage.admin_token) {
            xhr.setRequestHeader(
              "Authorization",
              "Bearer " + localStorage.admin_token
            );
          } else if (localStorage.token) {
            xhr.setRequestHeader("Authorization", "Bearer " + localStorage.token);
          }
        },
        contentType: "application/json",
        data:
          String(method).toLowerCase() === "get" ? data : JSON.stringify(data),
        success: function (response) {
          resolve(response);
        },
        error: function (error) {
          reject(error);
        },
      });
    });
};

const callFormAPI = (method, path, data) => {
  // 만약 data가 FormData 인스턴스가 아니면, 새 FormData로 변환
  const formData = data instanceof FormData
    ? data
    : Object.entries(data).reduce((fd, [key, value]) => {
        fd.append(key, value);
        return fd;
      }, new FormData());

  return new Promise((resolve, reject) => {
    $.ajax({
      url: path,
      type: method,
      beforeSend(xhr) {
        const token = localStorage.admin_token || localStorage.token;
        if (token) {
          xhr.setRequestHeader("Authorization", "Bearer " + token);
        }
      },
      contentType: false,
      processData: false,
      data: formData,
      success(response) {
        resolve(response);
      },
      error(error) {
        reject(error);
      }
    });
  });
};