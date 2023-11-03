const gestureZone = document.querySelector('.mainAnimatedPages');
let touchstartX = 0, touchstartY = 0, touchendX = 0, touchendY = 0;
let footerTimer; // Biến để lưu trữ timer cho việc tự động ẩn footer

gestureZone.addEventListener('touchstart', function(event) {
  touchstartX = event.changedTouches[0].screenX;
  touchstartY = event.changedTouches[0].screenY;
}, false);

gestureZone.addEventListener('touchend', function(event) {
  touchendX = event.changedTouches[0].screenX;
  touchendY = event.changedTouches[0].screenY;
  
  const delx = touchendX - touchstartX;
  const dely = touchendY - touchstartY;
  
  if (Math.abs(delx) < Math.abs(dely)) {
    if (dely < 0) {
    // Swipe down gesture: ẩn footer
      hideFooter();
    } else {
      // Swipe up gesture: hiển thị footer
      showFooter();
    }
  }
}, false);

gestureZone.addEventListener('wheel', function(event) {
  if (event.deltaY < 0) {
    // Scroll wheel down: ẩn footer
    hideFooter();
  } else {
    // Scroll wheel up: hiển thị footer
    showFooter();
  }
});

function showFooter() {
  clearTimeout(footerTimer); // Hủy timer để ngăn chặn việc tự động ẩn footer
  if (!isFooterVisible) {
    footer.style.opacity = '0';
    footer.style.display = 'block';
    setTimeout(function() {
      footer.style.opacity = '1';
    }, 10);
    isFooterVisible = true;
  }
  // Tự động ẩn footer sau 5 giây nếu không có tương tác
  footerTimer = setTimeout(function() {
    hideFooter();
  }, 5000);
}

function hideFooter() {
  if (isFooterVisible) {
    footer.style.opacity = '0';
    setTimeout(function() {
      footer.style.display = 'none';
    }, 500);
    isFooterVisible = false;
  }
}

// Lưu trạng thái hiển thị footer
let isFooterVisible = false;

// Lấy phần tử footer
const footer = document.querySelector('.smart-footer');
