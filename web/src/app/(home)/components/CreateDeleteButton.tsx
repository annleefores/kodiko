"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useSession } from "next-auth/react";
import { useToast } from "@/components/ui/use-toast";
import { Loader2 } from "lucide-react";

const CreateDeleteButton = () => {
  const router = useRouter();
  const { data: session } = useSession();
  const { toast } = useToast();

  interface podParams {
    pod_name: string;
    pod_id: string;
  }

  const [podData, setpodData] = useState<podParams>({
    pod_name: "",
    pod_id: "",
  });

  useEffect(() => {
    const podVal = localStorage.getItem("podData") || "";
    if (podVal !== "") {
      // decode base64 and convert to json
      const decodedPodData = JSON.parse(atob(podVal));
      setpodData(decodedPodData);
    }
  }, []);

  const ax = axios.create({
    baseURL: `${process.env.NEXT_PUBLIC_BACKEND}`,
    headers: {
      Authorization: `Bearer ${session?.accessToken}`,
    },
  });

  const errorToast = () => {
    toast({
      variant: "destructive",
      title: "Uh oh! Something went wrong.",
      description: "There was a problem with your request.",
    });
  };

  const createPod = async () => {
    try {
      const response = await ax.post("/create", { name: podData?.pod_name });
      console.log(response.data);
      localStorage.setItem("podData", response.data.pod_data);
      if (response.status === 200) {
        router.push("/code");
      }
    } catch (error) {
      console.log(error);
      errorToast();
    }
  };

  const deletePod = async () => {
    try {
      const response = await ax.post("/delete", { name: podData?.pod_name });
      console.log(response.data);
    } catch (error) {
      console.log(error);
      errorToast();
    }
  };

  return (
    <div className="flex flex-col md:flex-row gap-y-6 md:gap-x-12">
      <Button
        disabled={!session?.accessToken}
        onClick={createPod}
        className="bg-blue-500 hover:bg-blue-500 px-4 text-white rounded"
      >
        {!session?.accessToken ? (
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
        ) : (
          <></>
        )}
        Create Codepod
      </Button>
      <Button
        disabled={!session?.accessToken}
        onClick={deletePod}
        className="rounded px-4 bg-red-800 text-white hover:bg-red-800"
      >
        {!session?.accessToken ? (
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
        ) : (
          <></>
        )}
        Delete Codepod
      </Button>
    </div>
  );
};

export default CreateDeleteButton;
