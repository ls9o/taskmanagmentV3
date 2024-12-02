import { apiService } from "../Service/apiService";

// ฟังก์ชันสำหรับจัดรูปแบบวันที่
export function formatDateToThai(dateString: string, mode: number): string {
  const monthsShort = [
    "ม.ค.",
    "ก.พ.",
    "มี.ค.",
    "เม.ย.",
    "พ.ค.",
    "มิ.ย.",
    "ก.ค.",
    "ส.ค.",
    "ก.ย.",
    "ต.ค.",
    "พ.ย.",
    "ธ.ค.",
  ];

  const monthsFull = [
    "มกราคม",
    "กุมภาพันธ์",
    "มีนาคม",
    "เมษายน",
    "พฤษภาคม",
    "มิถุนายน",
    "กรกฎาคม",
    "สิงหาคม",
    "กันยายน",
    "ตุลาคม",
    "พฤศจิกายน",
    "ธันวาคม",
  ];

  const [datePart, timePart] = dateString.split(" ");
  const [year, month, day] = datePart.split("-").map(Number);
  const thaiYear = year + 543;
  const time = timePart ? timePart : "00:00:00"; // ถ้าไม่มีเวลาให้ตั้งค่าเป็น 00:00:00

  switch (mode) {
    case 1: // วันเดือนปี พ.ศ.
      return `${day}/${month}/${thaiYear} `;

    case 2: // วันเดือนปี พ.ศ. เดือนย่อแบบไทย
      return `${day} ${monthsShort[month - 1]} ${thaiYear}`;

    case 3: // วันเดือนปี พ.ศ. เดือนเต็มแบบไทย
      return `${day} ${monthsFull[month - 1]} ${thaiYear}`;

    case 4: // วันเดือนปี พ.ศ.
      return `${day}/${month}/${thaiYear} ${time}`;

    case 5: // วันเดือนปี พ.ศ. เดือนย่อแบบไทย
      return `${day} ${monthsShort[month - 1]} ${thaiYear} ${time}`;

    case 6: // วันเดือนปี พ.ศ. เดือนเต็มแบบไทย
      return `${day} ${monthsFull[month - 1]} ${thaiYear} ${time}`;

    default:
      return `Invalid mode.`;
  }
}
export function timeToInt(t: string): number {
  const [t_h, t_m, s] = t.split(":").map(Number);
  return t_h * 10000 + t_m * 100 + s;
}
export function timeToSec(t: string): number {
  const [h, m, s] = t.split(":").map(Number);
  return h * 3600 + m * 60 + s;
}
export function timeDiff(t1: string, t2: string): number {
  return timeToSec(t2) - timeToSec(t1);
}
// ฟังก์ชันเพื่อแปลงหมายเลขเดือนเป็นชื่อเดือนแบบเต็ม
export function monthName(month: number): string {
  switch (month) {
    case 1:
      return "มกราคม";
    case 2:
      return "กุมภาพันธ์";
    case 3:
      return "มีนาคม";
    case 4:
      return "เมษายน";
    case 5:
      return "พฤษภาคม";
    case 6:
      return "มิถุนายน";
    case 7:
      return "กรกฎาคม";
    case 8:
      return "สิงหาคม";
    case 9:
      return "กันยายน";
    case 10:
      return "ตุลาคม";
    case 11:
      return "พฤศจิกายน";
    case 12:
      return "ธันวาคม";
    default:
      return "เดือนที่ไม่ถูกต้อง";
  }
}
// ฟังก์ชันเพื่อแปลงหมายเลขเดือนเป็นชื่อเดือนย่อ
export function monthNameShort(month: number): string {
  switch (month) {
    case 1:
      return "ม.ค.";
    case 2:
      return "ก.พ.";
    case 3:
      return "มี.ค.";
    case 4:
      return "เม.ย.";
    case 5:
      return "พ.ค.";
    case 6:
      return "มิ.ย.";
    case 7:
      return "ก.ค.";
    case 8:
      return "ส.ค.";
    case 9:
      return "ก.ย.";
    case 10:
      return "ต.ค.";
    case 11:
      return "พ.ย.";
    case 12:
      return "ธ.ค.";
    default:
      return "เดือนที่ไม่ถูกต้อง";
  }
}
// ฟังก์ชันเพื่อแปลงวันในสัปดาห์เป็นชื่อวัน
export function weekdayName(weekday: string): string {
  switch (weekday) {
    case "Mon":
      return "จันทร์";
    case "Tue":
      return "อังคาร";
    case "Wed":
      return "พุธ";
    case "Thu":
      return "พฤหัสบดี";
    case "Fri":
      return "ศุกร์";
    case "Sat":
      return "เสาร์";
    case "Sun":
      return "อาทิตย์";
    default:
      return "วันที่ไม่ถูกต้อง";
  }
}
// ฟังก์ชันเพื่อแปลงหมายเลขวันในสัปดาห์เป็นชื่อวัน
export function weekdayNameShort(weekday: string): string {
  switch (weekday) {
    case "0":
      return "อาทิตย์";
    case "1":
      return "จันทร์";
    case "2":
      return "อังคาร";
    case "3":
      return "พุธ";
    case "4":
      return "พฤหัสบดี";
    case "5":
      return "ศุกร์";
    case "6":
      return "เสาร์";
    default:
      return "วันที่ไม่ถูกต้อง";
  }
}
// ฟังก์ชันเพื่อแปลงวันในสัปดาห์เป็นหมายเลข
export function weekdayNum(weekday: string): number {
  switch (weekday) {
    case "Mon":
      return 1;
    case "Tue":
      return 2;
    case "Wed":
      return 3;
    case "Thu":
      return 4;
    case "Fri":
      return 5;
    case "Sat":
      return 6;
    case "Sun":
      return 7;
    default:
      return 0;
  }
}
// ฟังก์ชันเพื่อหาคงาม
export function daysBetween(date1: string, date2: string): number {
  const startDate = new Date(date1);
  const endDate = new Date(date2);
  const diffTime = Math.abs(endDate.getTime() - startDate.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  // return diffDays+1;
  return diffDays;
}
export function toDays(date: number | string): number {
  const baseDate = 719528;

  if (typeof date === "number") {
    return baseDate + Math.floor(date / 86400);
  } else {
    const timestamp = Date.parse(date);
    if (isNaN(timestamp)) {
      throw new Error("Invalid date format");
    }
    return baseDate + Math.floor(timestamp / 86400000); // แปลงวินาทีเป็นวัน
  }
}

export function fromDays(daystamp: number, asTS = false): number | string {
  const baseDate = 719528;
  const timestamp = (daystamp - baseDate) * 86400;

  if (asTS) {
    return timestamp;
  } else {
    return new Date(timestamp * 1000).toISOString().split("T")[0]; // คืนค่าในรูปแบบ 'YYYY-MM-DD'
  }
}
export function progressPercentage(Process: any[] | null, subProcess: any[] | null): number {
  let totalCompletedDays = 0;
  let totalDays = 0;

  if (Process && Array.isArray(Process)) {
    Process.forEach((process) => {
      // ตรวจสอบว่าค่า processisvisible เป็น false หรือไม่
      if (process.processisvisible === false) {
        // รวมค่า processtart ของทุก process ที่ processisvisible เป็น false
        const processStartValue = process.processtart || 0;
        totalDays += processStartValue;

        // ตรวจสอบว่า subprocess เป็น array ที่มีค่า และมี subprocess ที่เชื่อมกับ process นี้หรือไม่
        const relatedSubProcesses = subProcess && Array.isArray(subProcess)
          ? subProcess.filter((sub) => sub.idprocess === process.id)
          : [];

        // ถ้ามี subprocess เชื่อมต่อกับ process ให้คำนวณค่าจาก processtart
        if (relatedSubProcesses.length > 0) {
          totalCompletedDays += processStartValue; // ใช้ค่า processtart ที่ทำแล้ว
        }
      }
    });
  }

  // คำนวณเปอร์เซ็นต์ความคืบหน้า
  return totalDays > 0
    ? Math.round((totalCompletedDays / totalDays) * 100) // ปัดเศษเป็นจำนวนเต็ม
    : 0; // คืนค่า 0 แทน
}


// export function progressPercentage(Process: any[] | null, subProcess: any[]): string {
//   let totalCompletedDays = 0;
//   let totalDays = 0;

//   if (Process && Array.isArray(Process)) {
//     Process.forEach((process) => {
//       // ตรวจสอบว่าค่า processisvisible เป็น false หรือไม่
//       if (process.processisvisible === false) {
//         // รวมค่า processtart ของทุก process ที่ processisvisible เป็น false
//         const processStartValue = process.processtart || 0;
//         totalDays += processStartValue;

//         // ตรวจสอบว่ามี subprocess ที่เชื่อมกับ process นี้หรือไม่
//         const relatedSubProcesses = subProcess.filter(
//           (sub) => sub.idprocess === process.id
//         );

//         // ถ้ามี subprocess เชื่อมต่อกับ process ให้คำนวณค่าจาก processtart
//         if (relatedSubProcesses.length > 0) {
//           totalCompletedDays += processStartValue; // ใช้ค่า processtart ที่ทำแล้ว
//         }
//       }
//     });
//   }

//   // คำนวณเปอร์เซ็นต์ความคืบหน้า
//   return totalDays > 0
//     ? ((totalCompletedDays / totalDays) * 100).toFixed(2)
//     : "0.00";
// }


// หา%ตามวัน
// export function progressPercentage(
//   dayDiff: number,
//   Process: any[] | null,
//   subProcess: any[]
// ): string {
//   let totalCompletedDays = 0;
//   const totalDays = dayDiff;

//   if (Process && Array.isArray(Process)) {
//     Process.forEach((process) => {
//       // ตรวจสอบว่ามี subprocess ที่เชื่อมกับ process นี้หรือไม่
//       const relatedSubProcesses = subProcess.filter(
//         (sub) => sub.idprocess === process.id
//       );

//       // ถ้ามี subprocess เชื่อมต่อกับ process ให้คำนวณค่าจาก processtart
//       if (relatedSubProcesses.length > 0) {
//         totalCompletedDays += process.processtart || 0; // ใช้ค่า processtart
//       }
//     });
//   }
//   // คำนวณเปอร์เซ็นต์ความคืบหน้า
//   return totalDays > 0
//     ? ((totalCompletedDays / totalDays) * 100).toFixed(2)
//     : "0.00";
// }
// หาความคืบหน้าจริง

// export function Checkstatus(taskDetail: any): string {
//   const currentDate = new Date();
//   const endDate = new Date(taskDetail.infoend);
//   const startDate = new Date(taskDetail.infostart);
//   if (!taskDetail) return "unknown";

//   if (currentDate < startDate) {
//     return "in coming";
//   } else if (currentDate > endDate) {
//     return "done";
//   } else {
//     return "processing";
//   }
// }
export function CheckProgressPercentage(taskDetail: any): number | string {
  if (!taskDetail) return "unknown";

  const currentDate = new Date();
  const startDate = new Date(taskDetail.infostart);
  const endDate = new Date(taskDetail.infoend);

  // ถ้า currentDate ยังไม่ถึงวันที่เริ่ม
  if (currentDate < startDate) {
    return 0; // ยังไม่เริ่ม
  }

  // คำนวณจำนวนวันทั้งหมด (นับเป็นวันเต็ม)
  const totalDays = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));

  // ถ้าจำนวนวันเป็น 0 หรือวันเริ่มเท่ากับวันสิ้นสุด
  if (totalDays === 0) {
    return currentDate >= startDate ? 100 : 0; // task เริ่มและสิ้นสุดในวันเดียวกัน
  }

  // คำนวณจำนวนวันที่ทำไปแล้ว (นับเป็นวันเต็ม)
  const completedDays = Math.ceil((currentDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));

  // คำนวณเปอร์เซ็นต์ความคืบหน้า
  let progressPercentage = (completedDays / totalDays) * 100;

  // ถ้า currentDate เกินวันที่สิ้นสุด ให้เกิน 100%
  if (currentDate > endDate) {
    progressPercentage = 100 + (completedDays - totalDays) / totalDays * 100;
  }

  // return ค่าความคืบหน้าแบบเปอร์เซ็นต์ (ปัดเศษเป็นจำนวนเต็ม)
  return Math.round(progressPercentage);
}

// export function CheckProgressPercentage(taskDetail: any): string {
//   if (!taskDetail) return "unknown";

//   const currentDate = new Date();
//   const startDate = new Date(taskDetail.infostart);
//   const endDate = new Date(taskDetail.infoend);

//   // ถ้า currentDate ยังไม่ถึงวันที่เริ่ม
//   if (currentDate < startDate) {
//     return "0.00"; // ยังไม่เริ่ม
//   }

//   // คำนวณจำนวนวันทั้งหมด (นับเป็นวันเต็ม)
//   const totalDays = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
  
//   // ถ้าจำนวนวันเป็น 0 หรือวันเริ่มเท่ากับวันสิ้นสุด
//   if (totalDays === 0) {
//     return currentDate >= startDate ? "100.00" : "0.00"; // task เริ่มและสิ้นสุดในวันเดียวกัน
//   }

//   // คำนวณจำนวนวันที่ทำไปแล้ว (นับเป็นวันเต็ม)
//   const completedDays = Math.ceil((currentDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));

//   // คำนวณเปอร์เซ็นต์ความคืบหน้า
//   let progressPercentage = (completedDays / totalDays) * 100;

//   // ถ้า currentDate เกินวันที่สิ้นสุด ให้เกิน 100%
//   if (currentDate > endDate) {
//     progressPercentage = 100 + (completedDays - totalDays) / totalDays * 100;
//   }

//   // return ค่าความคืบหน้าแบบเปอร์เซ็นต์
//   return progressPercentage.toFixed(2);
// }



interface CalendarEvent {
  id: string;
  title: string;
  start: string;
  end?: string;
  allDay?: boolean;
  priority: number;
}

let eventGuid = 0
const todayStr = new Date().toISOString().replace(/T.*$/, '') // YYYY-MM-DD of today

export const INITIAL_EVENTS: CalendarEvent[] = [
  {
    id: createEventId(),
    title: 'All-day event',
    start: todayStr,
    end: new Date(new Date(todayStr).setDate(new Date(todayStr).getDate() + 3)).toISOString().replace(/T.*$/, ''),
    priority: 1
},
{
    id: createEventId(),
    title: 'Workshop',
    start: `${todayStr}T09:00:00`,
    end: `${todayStr}T17:00:00`,
    priority: 2
},
]

export function createEventId() {
  return String(eventGuid++)
}


export * from "./function.inc";
