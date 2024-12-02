<template>
  <header class="header-menu-container d-flex justify-content-between align-items-center p-3">
    <!-- ปุ่มขีดขีดทางด้านซ้าย -->
    <button class="btn btn-outline-secondary" @click="toggleSidebar">
      <i class="pi pi-bars "></i>
    </button>

    <!-- เมนูกลาง และรูปโปรไฟล์ด้านขวาสุด -->
    <div class="d-flex align-items-center ms-auto">
      <nav class="menu d-none d-md-block">
        <ul class="navbar-nav flex-row">
          <li class="nav-item ">
            <router-link to="/" exact-active-class="active-link" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item ">
            <router-link to="/about" exact-active-class="active-link" class="nav-link">About</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/hello" exact-active-class="active-link" class="nav-link">Hello</router-link>
          </li>
          <li class="nav-item ">
            <router-link to="/show" exact-active-class="active-link" class="nav-link">Show</router-link>
          </li>
          <li class="nav-item ">
            <router-link to="/book" exact-active-class="active-link" class="nav-link">Book</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/assetssale" exact-active-class="active-link" class="nav-link">Assets Sale</router-link>
          </li>
        </ul>
      </nav>

      <!-- รูปโปรไฟล์ด้านขวาสุด -->
      <div class="dropdown ms-3">
        <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
          <img
            src="https://via.placeholder.com/40"
            alt="โปรไฟล์"
            class="profile-image rounded-circle"
            width="40"
            height="40"
          />
        </button>
        <ul class="dropdown-menu dropdown-menu-end">
          <li><a class="dropdown-item" href="#">โปรไฟล์</a></li>
          <li><a class="dropdown-item" href="#">ออกจากระบบ</a></li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script lang="ts" setup>
import { defineEmits } from 'vue';

const emit = defineEmits(['toggleSideMenu']);

function toggleSidebar() {
  emit('toggleSideMenu');
}
</script>

<style lang="scss" scoped>

.header-menu-container {
  border-bottom: 1px solid #dee2e6;

  .menu {
    ul {
      list-style: none;
      padding: 0;
      margin: 0;
      li{
        border-bottom:none;
      }

      .nav-item {
        .nav-link {
          padding: 5px 10px;
          position: relative;

          // เส้นขอบล่างพื้นฐาน (ซ่อนเส้น)
          &::after {
            content: '';
            position: absolute;
            bottom: -12px;
            left: 0;
            width: 0; // เริ่มต้นจากเส้นขนาด 0
            height: 5px;
            background-color: #1ca442; // สีฟ้า
            transition: width 0.4s ease; // ทำให้เส้นขยายจากทางซ้ายไปขวา
          }

          // เมื่อลิงก์ถูก active หรือ hover
          &.active-link,
          &:hover {
            color: #1ca442; // สีฟ้าเมื่อ active หรือ hover
            text-decoration: none;

            // ขยายเส้นจากซ้ายไปขวา
            &::after {
              width: 100%; // ขยายเส้นให้เต็มความกว้าง
            }
          }
        }
      }
    }
  }

  .dropdown {
    .profile-image {
      object-fit: cover;
      border: 2px solid #dee2e6;
      transition: border-color 0.3s ease;

      &:hover {
        border-color: #1ca442;
      }
    }

    .dropdown-toggle::after {
      margin-left: 10px;
    }
  }

  // ปรับสไตล์ของปุ่ม
  button {
    padding: 10px 15px; // ขนาดปุ่มใหญ่ขึ้น
    border: none; // ไม่มีเส้นขอบ
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #e2e6ea; // เปลี่ยนสีพื้นหลังเมื่อ hover
    }
  }
}

</style>