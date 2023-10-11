"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useSession } from "next-auth/react";

const CreateDeleteButton = () => {
  const router = useRouter();
  const { data: session } = useSession();

  interface podParams {
    pod_name: string;
    pod_id: string;
  }

  const [podData, setpodData] = useState<podParams>();

  // TODO: Add auth

  useEffect(() => {
    const podVal = localStorage.getItem("podName") || "";
    // decode base64 and convert to json
    const decodedPodData = JSON.parse(atob(podVal));
    setpodData(decodedPodData);
  }, []);

  const ax = axios.create({
    baseURL: `${process.env.NEXT_PUBLIC_BACKEND}`,
    headers: {
      Authorization: `Bearer ${session?.accessToken}`,
    },
  });

  const createPod = async () => {
    try {
      const response = await ax.post("/dummy", { name: podData?.pod_name });
      console.log(response.data);
      localStorage.setItem("podName", response.data.pod_data);
    } catch (error) {
      console.log(error);
    }
    router.push("/code");
  };

  const deletePod = async () => {
    try {
      const response = await ax.post("/delete", { name: podData?.pod_name });
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="flex flex-col md:flex-row gap-y-6 md:gap-x-12">
      <Button
        onClick={createPod}
        className="bg-blue-500 hover:bg-blue-500 px-6 text-white rounded"
      >
        Create Codepod
      </Button>
      <Button
        onClick={deletePod}
        className="rounded px-6 bg-red-800 text-white hover:bg-red-800"
      >
        Delete Codepod
      </Button>
    </div>
  );
};

export default CreateDeleteButton;
