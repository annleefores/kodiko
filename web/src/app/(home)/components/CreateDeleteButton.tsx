"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useSession } from "next-auth/react";

const CreateDeleteButton = () => {
  const router = useRouter();
  const { data: session } = useSession();

  const [podName, setpodName] = useState<String>("");

  // TODO: Add auth

  useEffect(() => {
    const podName = localStorage.getItem("podName") || "";
    setpodName(podName);
  }, []);

  const createPod = async () => {
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND}/create`,
        { name: podName }
      );
      console.log(response.data);
      localStorage.setItem("podName", response.data.pod_name);
    } catch (error) {
      console.log(error);
    }
    router.push("/code");
  };

  const deletePod = async () => {
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND}/delete`,
        { name: podName }
      );
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
