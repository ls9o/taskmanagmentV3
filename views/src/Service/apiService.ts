// src/services/apiService.ts

import axios from "axios";

// Create an Axios instance with a base URL
const apiClient = axios.create({
  baseURL: "http://localhost:8000/api", // Adjust this to your FastAPI URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Define API methods
export const apiService = {
  async login(credentials: { username: string; password: string }) {
    try {
      const response = await apiClient.post("/login", credentials);
      return response; // ทำการคืนค่าทั้งหมด
    } catch (error: any) {
      console.error(
        "Error during login API call:",
        error.response ? error.response.data : error.message
      );
      throw error;
    }
  },

  async getUser() {
    return apiClient.get("/users/");
  },
  // เพิ่มฟังก์ชัน postUser สำหรับการสร้างผู้ใช้ใหม่
  async postUser(userData: any) {
    return apiClient.post("/users/", userData);
  },
  async deleteUser(userID: number) {
    return apiClient.delete(`/users/${userID}`);
  },

  async query_user_by_id13(id: number) {
    return apiClient.get("/users/query/" + id);
  },
  async putUser_change_status(userId: number, Data: any) {
    return apiClient.put(`/users/${userId}`, Data);
  },
  async createItem(Data: any) {
    return apiClient.post("/users/", Data);
  },
  // Add other API methods as needed
  async getMenu() {
    return apiClient.get("/menu/");
  },
  async getOptions() {
    return apiClient.get("/options/");
  },
  async getOptions2() {
    return apiClient.get("/options2/");
  },
  async getEmployee() {
    return apiClient.get("/employee/");
  },
  async createEmployee(Data: any) {
    return apiClient.post("/employee/", Data);
  },
  async updataEmployee(employeeId: number, Data: any) {
    return apiClient.put(`/employee/${employeeId}`, Data);
  },
  async getLog(id: number | string | null = null) {
    const params: { id?: number | string } = {};
    if (id !== null) params.id = id; // ใช้ id เดียว
    return apiClient.get("/log/", {
      params: Object.keys(params).length ? params : undefined,
    });
  },
  async postLog(Data: any) {
    return apiClient.post("/log/", Data);
  },
  
  async getTask(userID: string | null = null, id: number | null = null) {
    // ใช้ type assertion เพื่อระบุประเภทของ params
    const params: { userID?: string | null; id?: number | null } = {};
    
    if (userID) {
      params.userID = userID;
    }
    if (id) {
      params.id = id;
    }
  
    // ส่ง request โดยใช้ params
    return apiClient.get("/tasks/", { params });
  }
,

  async getTaskuserandteam(usernamecodeserchuserandteam: string | null = null, id: number | null = null) {
    // ใช้ type assertion เพื่อระบุประเภทของ params
    const params: { usernamecodeserchuserandteam?: string | null; id?: number | null } = {};
  
    if (usernamecodeserchuserandteam) {
      params.usernamecodeserchuserandteam = usernamecodeserchuserandteam;
    }
    if (id) {
      params.id = id;
    }
  
    // ส่ง request โดยใช้ params
    return apiClient.get("/tasks/", { params });
  },
  // async getTask() {
  //   return apiClient.get("/tasks/");
  // },

  async postTask(item: any) {
    return apiClient.post("/tasks/", item);
  },

  async getTaskById(id: number) {
    return apiClient.get(`/tasks/${id}`);
  },

  async updateTask(taskId: number, taskData: any) {
    return apiClient.put(`/tasks/${taskId}`, taskData); // ใช้ PUT สำหรับการอัปเดต
  },
  async updatePercentageTask(taskId: number, taskData: any) {
    return apiClient.patch(`/tasks/${taskId}`, taskData); // ใช้ PATCH สำหรับการอัปเดตบางส่วน
  },
  async getProcess() {
    return apiClient.get("/process/");
  },
  async getProcessByTaskId(id: number) {
    return apiClient.get(`/process/${id}`);
  },
  async updateProcess(processId: number, processData: any) {
    return apiClient.put(`/processes/${processId}`, processData); // ใช้ PUT สำหรับการอัปเดต Process
  },
  async postProcess(item: object) {
    return apiClient.post("/process/", item);
  },
  async deleteProcess(processId: number) {
    return apiClient.delete(`/process/${processId}`);
  },

  async getSubProcess() {
    return apiClient.get("/subprocess/");
  },
  async postSubProcess(item: any) {
    return apiClient.post("/subprocess/", item);
  },
  async updateSubProcess(subprocessId: number, subprocessData: any) {
    return apiClient.put(`/subprocess/${subprocessId}`, subprocessData); // ใช้ PUT สำหรับการอัปเดต Process
  },
  
  async postSubtask(item: any) {
    return apiClient.post("/subtasks/", item)
  },
  async getSubtask() {
    return apiClient.get("/subtasks/")
  },
  async updateSubtask(subtasksId: number, subtasksData: any) {
    return apiClient.put(`/subtasks/${subtasksId}`,subtasksData);
  },

  async  postTeam(item: any) {
    return apiClient.post("/teams/", item);
  },

  async  getTeams() {
    return apiClient.get("/teams/");
  },
  async updateTeam(teamId: number, teamData: any) {
    return apiClient.put(`/teams/${teamId}`, teamData);
  },
  async  deleteTeams(teamId: number) {
    return apiClient.delete(`/teams/${teamId}`);
  },
};
